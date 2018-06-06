from hardware.qpcr import QpcrDataFile
from hardware.qpcr import get_amplification_data, get_ct, get_melt_data, get_tms
from app.models import ReagentGroupModel,ReagentModel
from .utilities import well_position_to_numeric,fetch_wells
from app.experiment_results.experiment_data_extractor import \
    fetch_allocation_results,fetch_reagent_categories




def parse_qpcr_file(plate_name,experiment_name,file):
    """
    Utility function to extract useful information to store from excel files
    containing QPCR experiment results

    Needs allocation results to trace ID plate well to its parent PA well
    Needs  the set of 'wells' under mentioned experiment ,plate to use
    as key to pick information from qpcr results

    Utilizes existing  QpcrDataFile class to extract data from qpcr
    results excel file
    """

    qpcr_reader = QpcrDataFile(file_name=plate_name)
    qpcr_results = qpcr_reader.get_data_by_well(file)
    allocation_results = fetch_allocation_results(experiment_name)
    wells = fetch_wells(allocation_results.plate_info[plate_name])
    experiment_results = get_experiment_results(wells,qpcr_results,
                                                plate_name,experiment_name)
    reagents_used,reagent_group_used =\
        get_reagents_groups(wells,allocation_results,plate_name)
    return experiment_results, reagents_used, reagent_group_used


def get_reagents_groups(wells,allocation_results,plate_name):
    reagents_used = {}
    reagent_group_used = {}
    reagent_categories=_fetch_reagent_categories()
    for well_id in wells:
        well_reagents, well_groups = \
            _get_reagents_groups_used(well_id, allocation_results,
                                      plate_name,reagent_categories)
        if well_reagents:
            reagents_used[well_id] = well_reagents
        if well_groups:
            reagent_group_used[well_id] = well_groups

    return reagents_used,reagent_group_used



def get_experiment_results(wells,qpcr_results,plate_name,experiment_name):
    experiment_results = []
    for well_id in wells:
        qpcr_well_meta = qpcr_results[well_id]
        refined_well = _refine_qpcr_well(qpcr_well_meta,plate_name,
                                         experiment_name)
        experiment_results.append(refined_well)

    return experiment_results

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------


def _refine_qpcr_well(qpcr_well,plate_name,experiment_name):
    """
    Extracts well properties that are part of QpcrResultsModel

    """
    temperatures = get_tms(qpcr_well)
    cycle_threshold = get_ct(qpcr_well)
    amplification_data = get_amplification_data(qpcr_well)
    melt_data = get_melt_data(qpcr_well)
    well = qpcr_well['well']

    return {
        'temperatures': temperatures,
        'cycle_threshold': cycle_threshold,
        'amplification_cycle': amplification_data['amplification_cycle'],
        'amplification_delta_rn':
            amplification_data['amplification_delta_rn'],
        'melt_temperature': melt_data['melt_temperature'],
        'melt_derivative': melt_data['melt_derivative'],
        'qpcr_well': well,
        'experiment': experiment_name,
        'qpcr_plate_id': plate_name,
    }



def _get_reagents_groups_used(qpcr_well,allocation_results,plate_name,
                              reagent_categories):
    """
    Extracts reagents and reagent groups from qpcr well , also extracts
    reagents, groups from source well if contents are transfered
    """
    row, col = well_position_to_numeric(qpcr_well)
    source_well = allocation_results.source_map[plate_name][
        col][row]

    if source_well:
        s_plate,s_row,s_col = _get_source_plate_row_col(source_well)
        well_source_allocation =\
            allocation_results.plate_info[s_plate][s_col][s_row]
        t_reagents,t_groups=_partition_reagents_groups(
            well_source_allocation,transfer=True,
            reagent_category=reagent_categories)
        reagents,groups = \
            get_allocation_reagents_groups(qpcr_well,
                                           allocation_results.plate_info[
                                               plate_name],reagent_categories)
        return t_reagents+reagents,t_groups+groups

    else:
        reagents, reagent_groups = \
            get_allocation_reagents_groups(qpcr_well,
                                           allocation_results.plate_info[
                                               plate_name],reagent_categories)

    return reagents, reagent_groups

def get_allocation_reagents_groups(qpcr_well,allocation_results,
                                   reagent_categories):

    row, col = well_position_to_numeric(qpcr_well)
    well_allocation = allocation_results[col][row]
    reagents, reagent_groups = _partition_reagents_groups(well_allocation,
                                                          transfer=False,
                                                          reagent_category=
                                                          reagent_categories)
    return reagents,reagent_groups

def _partition_reagents_groups(well_allocation, transfer,reagent_category):
    """
    Function partitions well contents into reagents and reagent groups.

    Reagent categories which belong to category_tags are only considered
    """
    reagents = []
    reagent_groups = []
    for (reagent, conc, unit) in well_allocation:
        if reagent in reagent_category:
            if reagent_category[reagent] in ['assay', 'template','human']:
                reagents.append({'reagent': reagent, 'transfer': transfer})
            elif reagent_category[reagent] == 'reagent_group':
                reagent_groups.append({'reagent_group': reagent,
                                       'transfer': transfer})
    return reagents, reagent_groups

def _get_source_plate_row_col(source_well):

    return source_well['source_plate'],source_well['source_row'],\
           source_well['source_col']

def _fetch_reagent_categories():
    """
    returns reagents and reagent groups from db , along with their
    category information
    """
    reagent_category = {r.name: r.category.name for r in
                        ReagentModel.objects.all()}
    reagent_category.update({r.group_name: 'reagent_group' for r in
                             ReagentGroupModel.objects.all()})
    return reagent_category