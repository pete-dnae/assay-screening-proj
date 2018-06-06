from app.experiment_results.experiment_data_extractor import  \
    get_qpcr_results_by_well ,get_labchip_results_by_well,get_labchip_plate_id

from app.experiment_results.qpcr_results_summary import \
    make_nested_idqpcr_datas
from clients.expt_recipes.nested.models import NestedMasterTable
from app.experiment_results.utilities import get_qpcr_labchip_well_map
from clients.expt_recipes.nested.models import NestedSummaryRow

def make_master_table(well_constituents, qpcr_query, labchip_query):

    qpcr_results = get_qpcr_results_by_well(qpcr_query)
    labchip_results = get_labchip_results_by_well(well_constituents,
                                                  labchip_query)
    qpcr_labchip_well_map = get_qpcr_labchip_well_map(qpcr_query,labchip_query)
    qpcr_record = qpcr_query.first()
    qpcr_plate_id = qpcr_record.qpcr_plate_id
    labchip_plate_id = get_labchip_plate_id(labchip_query)

    id_qpcr_datas = \
        make_nested_idqpcr_datas(well_constituents, qpcr_results)
    master_table = \
        NestedMasterTable.create_from_db(qpcr_plate_id, labchip_plate_id,
                                         qpcr_labchip_well_map,
                                         well_constituents,
                                         id_qpcr_datas, labchip_results)

    return master_table

def make_summary_table(master_table):

    grps = {}
    for r in master_table:
        grp_key = (r['ID Template Name'], r['ID Template Conc.'],
                   r['ID Human Name'], r['ID Human Conc.'],
                   r['PA Assay Name'],
                   r['PA Template Name'], r['PA Template Conc.'],
                   r['PA Human Name'], r['PA Human Conc.']
                   )
        grps.setdefault(grp_key, []).append(r)

    summary_rows = []
    for g in grps:
        summary_rows.append(
            NestedSummaryRow.create_from_master_table_rows(grps[g]))
    return summary_rows

