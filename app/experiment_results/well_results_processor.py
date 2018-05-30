from app.models.labchip_results_model import LabChipResultsModel
from app.models.qpcr_results_model import QpcrResultsModel
from .well_constituents_maker import WellConstituentsMaker
from .qpcr_results_summary import WellsSummaryMaker
from clients.expt_recipes.nested.models import NestedMasterTable
from clients.expt_recipes.vanilla.models import VanillaMasterTable
from clients.expt_recipes.vanilla.models import VanillaSummaryRow
from .graph_data_processor import GraphDataProcessor
from clients.expt_recipes.lost import build_labchip_datas_from_inst_data
from .experiment_data_extractor import get_qpcr_well_ids,\
    get_qpcr_results_by_well,get_qpcr_well_lookup,\
    get_labchip_results_from_queryset,get_labchip_wells,\
    get_labchip_palate_id,fetch_allocation_results,fetch_reagent_categories,\
    fetch_assay_amplicon_lengths,get_dilutions


def build_well_constituents(plate_id, qpcr_wells, allocation_results,
                            reagent_categories):

    well_constituents_maker = \
        WellConstituentsMaker(plate_id, qpcr_wells, allocation_results,
                              reagent_categories)
    well_constituents = well_constituents_maker.prepare_well_constituents()
    return well_constituents


def build_labchip_results(allocation_results, labchip_plate_id,
                          labchip_wells, well_constituents, lab_chip_results,
                          qpcr_labchip_well_lookup, reagent_amplicon_lengths):
    lab_chip_plate_allocation = allocation_results.plate_info[labchip_plate_id]
    dilutions = get_dilutions(lab_chip_plate_allocation, labchip_wells)
    labchip_results = build_labchip_datas_from_inst_data(
        well_constituents, lab_chip_results, qpcr_labchip_well_lookup,
        reagent_amplicon_lengths, dilutions)
    return labchip_results


def get_nested_master_table(well_summary_maker, plate_id, labchip_plate_id,
                            qpcr_labchip_well_lookup, well_constituents,
                            labchip_results):
    qpcr_summary = well_summary_maker.prepare_nested_summary()
    master_table = NestedMasterTable.create_from_db(plate_id,
                                           labchip_plate_id,
                                           qpcr_labchip_well_lookup,
                                           well_constituents,
                                           qpcr_summary,
                                           labchip_results)
    return master_table


def get_vanilla_master_table(well_summary_maker, qpcr_wells, plate_id,
                             labchip_wells, labchip_plate_id,
                             well_constituents, labchip_results):
    qpcr_summary = well_summary_maker.prepare_vanilla_summary()
    master_table = VanillaMasterTable. create_from_db(qpcr_wells, plate_id,
                                                      labchip_wells,
                                                      labchip_plate_id,
                                                      well_constituents,
                                                      qpcr_summary,
                                                      labchip_results)
    return master_table


def create_summary_rows(master_table):
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


class WellResultsAggregation:

    def __init__(self):
        self.master_table_rows = None
        self.summary_table_rows = None
        self.amp_melt_graph = None
        self.copy_cnt_graph = None
        self.lab_chip_results = None


    @classmethod
    def create(cls, experiment_type, plate_id, qpcr_wells, labchip_wells,
               qpcr_results,allocation_results,qpcr_labchip_well_lookup,
               reagent_categories,reagent_amplicon_lengths, labchip_plate_id,
               lab_chip_results):

        well_constituents = build_well_constituents(plate_id, qpcr_wells,
                                                    allocation_results,
                                                    reagent_categories)

        labchip_results = build_labchip_results(allocation_results,
                                                labchip_plate_id,
                                                labchip_wells,
                                                well_constituents,
                                                lab_chip_results,
                                                qpcr_labchip_well_lookup,
                                                reagent_amplicon_lengths)
        well_summary_maker = WellsSummaryMaker(well_constituents, qpcr_results)
        if experiment_type=='nested':
            master_table = get_nested_master_table(well_summary_maker,
                                                   plate_id,
                                                   labchip_plate_id,
                                                   qpcr_labchip_well_lookup,
                                                   well_constituents,
                                                   labchip_results)
        else:
            master_table = get_vanilla_master_table(well_summary_maker,
                                                    qpcr_wells, plate_id,
                                                    labchip_wells,
                                                    labchip_plate_id,
                                                    well_constituents,
                                                    labchip_results)

        summary_rows = create_summary_rows(master_table)


        graphDataProcessor = GraphDataProcessor(well_constituents, qpcr_results)
        inst = cls()
        inst.master_table_rows = master_table.rows
        inst.summary_table_rows = summary_rows
        inst.amp_melt_graph = graphDataProcessor.prepare_amp_melt_graph()
        inst.copy_cnt_graph = graphDataProcessor.prepare_copy_count_graph()
        inst.lab_chip_results = labchip_results
        return inst

    @classmethod
    def create_from_wells(cls,  expt_id, plate_id,wells):
        qpcr_results_queryset = QpcrResultsModel.objects.filter(
            experiment_id=expt_id, qpcr_plate_id=plate_id,qpcr_well__in=wells)

        qpcr_well_db_id_map = get_qpcr_well_ids(qpcr_results_queryset)

        lab_chip_results_queryset = LabChipResultsModel.objects.filter(
            qpcr_well__in=qpcr_well_db_id_map.keys())

        inst = cls.create(
            expt_id,plate_id,wells,
            get_labchip_wells(lab_chip_results_queryset),
            get_qpcr_results_by_well(qpcr_results_queryset),
            fetch_allocation_results(expt_id),
            get_qpcr_well_lookup(lab_chip_results_queryset,
                                 qpcr_well_db_id_map),
            fetch_reagent_categories(),
            fetch_assay_amplicon_lengths(),
            get_labchip_palate_id(lab_chip_results_queryset),
            get_labchip_results_from_queryset(lab_chip_results_queryset))

        return inst

