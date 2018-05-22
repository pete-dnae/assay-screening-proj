from hardware.qpcr import QpcrDataFile
from hardware.qpcr import get_amplification_data, get_ct, get_melt_data, get_tms
from hardware.labchip_peak import LabChipPeakProcessor
from app.models.qpcr_results_model import QpcrResultsModel
from app.models.reagent_model import ReagentModel
from app.models.units_model import UnitsModel
from app.models.reagent_group_model import ReagentGroupModel
from app.models.experiment_model import ExperimentModel
from app.rules_engine.rule_script_processor import RulesScriptProcessor
from django.shortcuts import get_object_or_404
import re
import math
from .labchip_results_processor import UnexpectedWellNameError


class QpcrResultsProcessor():
    """
    Utility class to extract useful information to store from excel
    files
    containing QPCR experiment results
    """

    def __init__(self, plate_name, experiment_name, category_tags):
        """
         Needs allocation results to trace ID plate well to its parent PA well
         Needs  the set of 'wells' under mentioned experiment ,plate to use
         as key to pick information from qpcr results
         """

        self.plate_name = plate_name
        self.experiment_name = experiment_name
        self.category_tags = category_tags
        self.allocation_results = self._fetch_allocation_results()
        self.wells = self._fetch_wells()
        self.reagent_category = self._fetch_reagent_categories()

    def parse_qpcr_file(self, file):
        """
        Utilizes existing  QpcrDataFile class to extract data from qpcr
        results excel file
        """

        qpcr_reader = QpcrDataFile(file_name=self.plate_name)
        qpcr_results = qpcr_reader.get_data_by_well(file)
        experiment_results = []
        reagents_used = {}
        reagent_group_used = {}
        for well_id in self.wells:
            qpcr_well = qpcr_results[well_id]
            refined_well = self._refine_qpcr_well(qpcr_well)
            experiment_results.append(refined_well)
            well_reagents, well_groups = self._get_reagents_groups_used(well_id)
            if well_reagents:
                reagents_used[well_id] = well_reagents
            if well_groups:
                reagent_group_used[well_id] = well_groups
        return experiment_results, reagents_used, reagent_group_used

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _refine_qpcr_well(self, qpcr_well):
        """
        Extracts well properties that are part of QpcrResultsModel

        """
        temperatures = get_tms(qpcr_well)
        cycle_threshold = get_ct(qpcr_well)
        amplification_data = get_amplification_data(qpcr_well)
        melt_data = get_melt_data(qpcr_well)
        well = qpcr_well['well']
        experiment = qpcr_well['expt']

        return {
            'temperatures': temperatures,
            'cycle_threshold': cycle_threshold,
            'amplification_cycle': amplification_data['amplification_cycle'],
            'amplification_delta_rn':
                amplification_data['amplification_delta_rn'],
            'melt_temperature': melt_data['melt_temperature'],
            'melt_derivative': melt_data['melt_derivative'],
            'qpcr_well': well,
            'experiment': experiment,
            'qpcr_plate_id': self.plate_name,
        }

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

    def _fetch_reagent_categories(self):
        """
        returns reagents and reagent groups from db , along with their
        category information
        """
        reagent_category = {r.name: r.category.name for r in
                            ReagentModel.objects.all()}
        reagent_category.update({r.group_name: 'reagent_group' for r in
                                 ReagentGroupModel.objects.all()})
        return reagent_category

    def _fetch_experiment(self):
        """"
          Fetches experiment object from db , returns http:404 if not fould
        """
        return get_object_or_404(ExperimentModel, pk=self.experiment_name)

    def _well_position_to_alpha_numeric(self, well_position):
        """
        Converts well position from numeric to alphanumeric
        """

        row, col = well_position
        strcol = str(col).zfill(2)
        strrow = chr(row + 64)
        return strrow + strcol

    def _fetch_wells(self):
        """
        Extracts keys from allocation_results and convert them into
        corresponding alphanumeric well_name representations
        """
        wells = []
        source_map = self.allocation_results.plate_info[self.plate_name]
        for col, rows in source_map.items():
            wells_in_row = [self._well_position_to_alpha_numeric((row, col)) for
                            row in rows.keys()]
            wells = wells + wells_in_row
        return set(wells)

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

    def _get_reagents_groups_used(self, qpcr_well):
        """
        Extracts reagents and reagent groups from qpcr well , also extracts
        reagents, groups from source well if contents are transfered
        """
        row, col = self._well_position_to_numeric(qpcr_well)
        source_well = self.allocation_results.source_map[self.plate_name][
            col][row]

        if source_well:
            s_plate,s_row,s_col = self._get_source_plate_row_col(source_well)
            well_source_allocation = self._get_well_allocation(s_plate,s_row,s_col)
            well_current_allocation = self._get_well_allocation(
                self.plate_name, row, col)
            t_reagents,t_groups=self._partition_reagents_groups(
                well_source_allocation,transfer=True)
            reagents,groups = self._partition_reagents_groups(
                well_current_allocation,transfer=False)

            return t_reagents+reagents,t_groups+groups

        transfer = False
        well_allocation = self._get_well_allocation(self.plate_name, row,
                                                    col)

        return self._partition_reagents_groups(well_allocation, transfer)

    def _get_well_allocation(self, plate, row, col):

        return self.allocation_results.plate_info[plate][col][row]

    def _partition_reagents_groups(self, well_allocation, transfer):
        """
        Function partitions well contents into reagents and reagent groups.

        Reagent categories which belong to category_tags are only considered
        """
        reagents = []
        reagent_groups = []
        for (reagent, conc, unit) in well_allocation:
            if reagent in self.reagent_category:
                if self.reagent_category[reagent] in self.category_tags:
                    reagents.append({'reagent': reagent, 'transfer': transfer})
                elif self.reagent_category[reagent] == 'reagent_group':
                    reagent_groups.append({'reagent_group': reagent,
                                           'transfer': transfer})
        return reagents, reagent_groups

    def _get_source_plate_row_col(self,source_well):

        return source_well['source_plate'],source_well['source_row'],\
               source_well['source_col']