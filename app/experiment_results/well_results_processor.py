from rest_framework.exceptions import ValidationError
from app.models.reagent_model import ReagentModel
from app.models.units_model import UnitsModel
from app.models.reagent_group_model import ReagentGroupModel
from app.models.experiment_model import ExperimentModel
from app.models.labchip_results_model import LabChipResultsModel
from app.models.qpcr_results_model import QpcrResultsModel
from app.rules_engine.rule_script_processor import RulesScriptProcessor
from .well_constituents_maker import WellConstituentsMaker
from .qpcr_results_summary import WellsSummaryMaker
from .labchip_results_summary import LabchipResultsSummary
from django.shortcuts import get_object_or_404
from clients.expt_recipes.nested.models import NestedMasterTable
from clients.expt_recipes.vanilla.models import VanillaMasterTable
from clients.expt_recipes.vanilla.models import VanillaSummaryRow
from app.models.reagent_group_model import ReagentGroupDetailsModel
from collections import defaultdict
from .labchip_results_processor import UnexpectedWellNameError
from .graph_data_processor import GraphDataProcessor
import re
import json
from json.decoder import JSONDecodeError


class WellResultsProcessor:

    def __init__(self, experiment_name, plate_id, wells):
        self.experiment_name = experiment_name
        self.plate_id = plate_id
        self.qpcr_wells = wells
        self.labchip_wells = None
        self.qpcr_data = self._fetch_qpcr_data()
        self.allocation_results = self._fetch_allocation_results()
        self.reagent_data = self._fetch_reagent_data()
        self.labchip_data = None
        self.labchip_plate_id = None

    def fetch_well_results(self):

        well_constituents_maker = WellConstituentsMaker(self.plate_id,
                                                        self.qpcr_wells,
                                                        self.allocation_results,
                                                        self.reagent_data[
                                                            'category'])
        well_constituents = well_constituents_maker.prepare_well_constituents()
        well_summary = WellsSummaryMaker(well_constituents,
                                         self.qpcr_data['results'])

        qpcr_restuls = well_summary.prepare_nested_summary()
        self.labchip_data = self._fetch_labchip_data()
        dilutions = self._get_dilutions(self.labchip_wells)
        labchip_summary_maker = LabchipResultsSummary(
            dilutions, self.labchip_data['results'],
            well_constituents, self.labchip_data['well_ids'], self.reagent_data[
                'amplicon_lengths'])
        labchip_results = labchip_summary_maker.fetch_labchip_results()

        results = NestedMasterTable.create_from_db(self.plate_id,
                                                   self.labchip_plate_id,
                                                   self.labchip_data[
                                                       'well_ids'],
                                                   well_constituents,
                                                   qpcr_restuls,
                                                   labchip_results)

        graphDataProcessor = GraphDataProcessor(well_constituents,
                                                self.qpcr_data['results'])
        amp_melt_graph = graphDataProcessor.prepare_amp_melt_graph()
        cpy_cnt_graph = graphDataProcessor.prepare_copy_count_graph()
        summary = self._get_calculations_summary(results)
        return {'master_table': results.rows,
                'summary_table': summary,
                'graphData':{
                    'amp_melt_graph':amp_melt_graph,
                    'cpy_cnt_graph':cpy_cnt_graph,
                    'labchip_peaks':self.labchip_data['results']
                }}

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _fetch_labchip_data(self):

        labchip_results_queryset = LabChipResultsModel.objects.filter(
            qpcr_well__in=self.qpcr_data['well_ids'].keys()
        )

        qpcr_labchip_lookup = self._get_qpcr_well_lookup(
            labchip_results_queryset)
        labchip_results = self._get_labchip_results_from_queryset(
            labchip_results_queryset)
        self.labchip_wells = self._get_labchip_wells(labchip_results_queryset)
        self.labchip_plate_id = self._get_labchip_palate_id(
            labchip_results_queryset)
        return {'results': labchip_results, 'well_ids': qpcr_labchip_lookup}

    def _fetch_qpcr_data(self):
        qpcr_result_queryset = QpcrResultsModel.objects.filter(
            experiment_id=self.experiment_name, qpcr_plate_id=self.plate_id,
            qpcr_well__in=self.qpcr_wells)

        qpcr_well_ids = self._get_qpcr_well_ids(qpcr_result_queryset)
        qpcr_results = self._get_qpcr_results_by_well(qpcr_result_queryset)

        return {'results': qpcr_results, 'well_ids': qpcr_well_ids}

    def _fetch_allocation_results(self):
        """
          Fetches experiment ,prepares allowed reagents and units.
          Co-ordinates interpretation of ruleScript to produce allocation
          results.
          Returns None if errors are present
        """
        experiment = self._fetch_experiment()
        reagent_names = [r.name for r in ReagentModel.objects.all()]

        group_names = set([g.group_name for g in \
                           ReagentGroupModel.objects.all()])

        allowed_names = reagent_names + list(group_names)
        units = [u.abbrev for u in UnitsModel.objects.all()]

        interpreter = RulesScriptProcessor(
            experiment.rules_script.text, allowed_names, units)
        parse_error, alloc_table, thermal_cycling_results, line_num_mapping = \
            interpreter.parse_and_interpret()

        return None if not alloc_table else alloc_table

    def _fetch_reagent_data(self):

        reagent_query_set = ReagentModel.objects.all()
        reagent_category = self._fetch_reagent_categories(reagent_query_set)
        assay_amplicon_lengths = self._fetch_assay_amplicon_lengths(
            reagent_query_set)
        return {'category': reagent_category,
                'amplicon_lengths': assay_amplicon_lengths}

    def _fetch_reagent_categories(self, query_set):
        """
        returns reagents and reagent groups from db , along with their
        category information
        """
        reagent_category = {r.name: r.category.name for r in
                            query_set}

        for r in ReagentGroupModel.objects.all():
            group_element = ReagentGroupDetailsModel.objects.filter(
                reagent_group=r.group_name).first()
            reagent_category[r.group_name] = group_element.reagent.category.name

        return reagent_category

    def _fetch_assay_amplicon_lengths(self, query_set):

        amplicon_len_dict = {}
        for element in query_set:
            json_string = element.opaque_json_payload
            if element.category.name == 'assay':
                try:
                    if json_string is None:
                        raise ValueError('opaque payload for assay not found')
                    meta_data = json.loads(json_string)
                    if 'amplicon_length' in meta_data:
                        amplicon_len_dict[element.name] = float(meta_data[
                                                                    'amplicon_length'])
                except JSONDecodeError:
                    raise ValidationError
        return amplicon_len_dict

    def _fetch_experiment(self):
        """"
          Fetches experiment object from db , returns http:404 if not fould
        """
        return get_object_or_404(ExperimentModel, pk=self.experiment_name)

    def _get_qpcr_well_ids(self, query_set):
        """
        Prepares a dictionary with well db id as key and well name as value
        """
        return {record['id']: record['qpcr_well'] for record in
                query_set.values('id', 'qpcr_well')}

    def _get_qpcr_results_by_well(self, query_set):
        """
        Prepares a dictionary with well name as key and well results as value
        """

        return {result['qpcr_well']: result for result in query_set.values()}

    def _get_qpcr_well_lookup(self, query_set):
        """
        Returns a dictionary keyes by qpcr wells with values corresponding to
        labchip wells
        """
        labchip_lookup_dict = {record['qpcr_well_id']: record['labchip_well']
                               for record in query_set.values('qpcr_well_id',
                                                              'labchip_well')}
        qpcr_lookup_dict = {}

        for qpcr_well_id, qpcr_well in self.qpcr_data['well_ids'].items():
            qpcr_lookup_dict[qpcr_well] = labchip_lookup_dict[qpcr_well_id] if \
                qpcr_well_id in labchip_lookup_dict else None

        return qpcr_lookup_dict

    def _get_labchip_results_from_queryset(self, query_set):
        """
        returns a restructured form of labchip resutls extractd from queryset
        """
        results = defaultdict(dict)

        for labchip in query_set.values():
            peak_dict = results[labchip['labchip_well']].setdefault('peak', {})
            key = labchip['peak_name']
            peak_dict[key] = {'%_purity': labchip['purity'],
                              'conc_(ng/ul)': labchip['concentration'],
                              'molarity_(nmol/l)': labchip['molarity'],
                              'size_[bp]': labchip['size']
                              }

        return results

    def _get_dilutions(self, labchip_wells):
        dilution_dict = {}
        for well_id in labchip_wells:
            row, col = self._well_position_to_numeric(well_id)
            well_allocation = self.allocation_results.plate_info[
                self.labchip_plate_id][col][row]
            dilutions = [conc for (reagent, conc, unit) in well_allocation if
                         unit == 'dilution']
            if len(dilutions) > 0:
                dilution_dict[well_id] = dilutions[0]
        return dilution_dict

    def _get_labchip_wells(self, query_set):

        return [result['labchip_well'] for result in query_set.values(
            'labchip_well')]

    def _well_position_to_numeric(self, well_position):
        """
        Converts well position from alphanumeric to numeric
        """

        match = re.match(r"([A-Z])([0-9]+)", well_position)

        if not match:
            raise UnexpectedWellNameError()

        try:
            row, col = match.groups()
            numrow = ord(row) - 64
            numcol = int(col)
            return numrow, numcol
        except:
            raise UnexpectedWellNameError()

    def _get_labchip_palate_id(self, query_set):

        labchip_record = query_set.first()
        if labchip_record:
            return labchip_record.labchip_plate_id

        return None

    def _get_calculations_summary(self,master_table):

        grps = {}

        for r in master_table.rows:
            grp_key = (r['ID Template Name'], r['ID Template Conc.'],
                       r['ID Human Name'], r['ID Human Conc.'])
            grps.setdefault(grp_key, []).append(r)

        srows = []
        for g in grps:
            srows.append(
                VanillaSummaryRow.create_from_master_table_rows(grps[g]))

        return srows