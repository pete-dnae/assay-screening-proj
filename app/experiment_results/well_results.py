from .experiment_data_extractor import fetch_allocation_results,\
    fetch_reagent_categories,fetch_assay_amplicon_lengths,get_qpcr_well_ids,\
    get_qpcr_well_lookup,get_labchip_palate_id,get_labchip_wells,\
    get_dilutions,get_plate_allocation,get_labchip_results_from_queryset,\
    fetch_experiment

from app.models.labchip_results_model import LabChipResultsModel
from app.models.qpcr_results_model import QpcrResultsModel
from app.experiment_results.qpcr_results_summary import QpcrSummaryMaker
from app.experiment_results.well_constituents_maker import WellConstituentsMaker
from clients.expt_recipes.lost import build_labchip_datas_from_inst_data
from clients.expt_recipes.nested.models import NestedMasterTable
from clients.expt_recipes.vanilla.models import VanillaMasterTable
from clients.expt_recipes.vanilla.models import VanillaSummaryRow
from .graph_data_processor import GraphDataProcessor

class WellResultsProcessor:
    """
    Class is responsible producing well results aggregation by creating well
    constituents ,extracting qpcr and labchip results and orchestrating the
    summary
    """

    def __init__(self,experiment_id,plate_id,wells):
        self.experiment_id = experiment_id
        self.plate_id = plate_id
        self.wells = wells
        self.allocation_results = fetch_allocation_results(experiment_id)
        self.reagent_categories = fetch_reagent_categories()
        self.assay_amplicon_lengths = fetch_assay_amplicon_lengths()
        self.qpcr_queryset = self._get_qpcr_queryset()
        self.well_constituents = self._build_well_constituents()



    def prepare_well_aggregation(self):

        master_table = self._prepare_master_table()
        summary_rows = self.create_summary_rows(master_table)
        graphDataProcessor = GraphDataProcessor(self.well_constituents,
                                                self.qpcr_queryset)
        amp_melt_graph = graphDataProcessor.prepare_amp_melt_graph()
        copy_count_graph = graphDataProcessor.prepare_copy_count_graph()





    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------


    def _prepare_master_table(self):
        qpcr_well_db_id_map = get_qpcr_well_ids(self.qpcr_queryset)
        labchip_query_set = LabChipResultsModel.objects.filter(
            qpcr_well__in=qpcr_well_db_id_map.keys())

        labchip_plate_id, labchip_wells,labchip_results=self._get_labchip_data(
            labchip_query_set)

        lab_chip_plate_allocation = get_plate_allocation(self.allocation_results
                                                         ,labchip_plate_id)

        dilutions = get_dilutions(lab_chip_plate_allocation, labchip_wells)

        qpcr_labchip_well_lookup = get_qpcr_well_lookup(labchip_query_set,
                                                        qpcr_well_db_id_map)
        labchip_results = self._build_labchip_results(dilutions,
                                                labchip_results,
                                                qpcr_labchip_well_lookup)
        well_summary_maker = QpcrSummaryMaker(self.well_constituents,
                                              self.qpcr_queryset)
        experiment_type = self._get_experiment_type()
        if experiment_type == 'nested':
            master_table = self.get_nested_master_table(well_summary_maker,
                                                        labchip_plate_id,
                                                   qpcr_labchip_well_lookup,
                                                   labchip_results)
        else:
            master_table = self.get_vanilla_master_table(well_summary_maker,
                                                    labchip_plate_id,
                                                    qpcr_labchip_well_lookup,
                                                    labchip_results)
        return master_table

    def _get_qpcr_queryset(self):

        return QpcrResultsModel.objects.filter(
            experiment_id=self.experiment_id, qpcr_plate_id=self.plate_id,
            qpcr_well__in=self.wells)

    def _get_labchip_data(self, labchip_query_set):
        labchip_plate_id = get_labchip_palate_id(labchip_query_set)
        labchip_wells = get_labchip_wells(labchip_query_set)
        labchip_results = get_labchip_results_from_queryset(labchip_query_set)
        return labchip_plate_id,labchip_wells,labchip_results

    def _build_well_constituents(self):
        well_constituents_maker = WellConstituentsMaker(self.plate_id,
                                                        self.wells,
                                                        self.allocation_results,
                                                        self.reagent_categories)
        well_constituents = well_constituents_maker.prepare_well_constituents()
        return well_constituents

    def _build_labchip_results(self,dilutions, lab_chip_results,
                               qpcr_labchip_well_lookup):
        reagent_amplicon_lengths = fetch_assay_amplicon_lengths()
        labchip_results = build_labchip_datas_from_inst_data(
            self.well_constituents, lab_chip_results, qpcr_labchip_well_lookup,
            reagent_amplicon_lengths, dilutions)
        return labchip_results

    def get_nested_master_table(self,well_summary_maker,
                                labchip_plate_id,
                                qpcr_labchip_well_lookup,
                                labchip_results):
        qpcr_summary = well_summary_maker.prepare_nested_summary()
        master_table = \
            NestedMasterTable.create_from_db(self.plate_id,
                                             labchip_plate_id,
                                             qpcr_labchip_well_lookup,
                                             self.well_constituents,
                                             qpcr_summary,
                                             labchip_results)
        return master_table


    def get_vanilla_master_table(self,well_summary_maker,  labchip_plate_id,
                                qpcr_labchip_well_lookup,
                                labchip_results):
        qpcr_summary = well_summary_maker.prepare_vanilla_summary()
        master_table =\
            VanillaMasterTable.create_from_db(self.plate_id,
                                              qpcr_labchip_well_lookup,
                                              labchip_plate_id,
                                              self.well_constituents,
                                              qpcr_summary,
                                              labchip_results)
        return master_table

    def _get_experiment_type(self):
        experiment_obj = fetch_experiment(self.experiment_id)
        return experiment_obj['experiment_type']

    def create_summary_rows(self,master_table):
        grps = {}
        for r in master_table.rows:
            grp_key = (r['ID Template Name'], r['ID Template Conc.'],
                       r['ID Human Name'], r['ID Human Conc.'])
            grps.setdefault(grp_key, []).append(r)

        summary_rows = []
        for g in grps:
            summary_rows.append(
                VanillaSummaryRow.create_from_master_table_rows(grps[g]))
        return summary_rows