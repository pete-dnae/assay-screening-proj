from app.experiment_results.nested.builder import make_master_table as \
    make_nested_master_table
from app.experiment_results.vanilla.builder import make_master_table as \
    make_vanilla_master_table
from app.experiment_results.nested.builder import make_summary_table as \
    make_nested_summary_table
from app.experiment_results.vanilla.builder import make_summary_table as \
    make_vanilla_summary_table
from .experiment_data_extractor import  get_labchip_query, \
    fetch_allocation_results, fetch_reagent_categories,\
    get_labchip_results_from_queryset

from .well_constituents_maker import make_well_constituents

from .graph_data_processor import prepare_amp_graph, prepare_copy_count_graph, \
    prepare_melt_graph


class QpcrWellAggregation:
    """
    Coordinates various function to produce vanilla or nested summary based
    on experiment type provided , also coordinates retrieval of data for graphs
    """

    def __init__(self):
        self.summary_table = None
        self.master_table = None
        self.amp_graph = None
        self.melt_graph = None
        self.copy_cnt_graph = None
        self.labchip_peaks = None

    @classmethod
    def create(cls, summary_table, master_table, amp_graph, melt_graph,
               copy_cnt_graph, labchip_peaks):
        inst = cls()
        inst.summary_table = summary_table
        inst.master_table = master_table
        inst.amp_graph = amp_graph
        inst.melt_graph = melt_graph
        inst.copy_cnt_graph = copy_cnt_graph
        inst.labchip_peaks = labchip_peaks

        return inst.__dict__

    @classmethod
    def create_from_query(cls, qpcr_query):
        """
         Accepts qpcr query to retrieve associated labchip info in  labchip
         query and allocation results for wells under qpcr query in well
         constituents
        """
        labchip_query = get_labchip_query(qpcr_query)
        well_constituents = get_well_constituents(qpcr_query)
        master_table = get_master_table(well_constituents, qpcr_query,
                                         labchip_query)
        summary_table = create_summary_rows(master_table,qpcr_query)
        amp_graph = prepare_amp_graph(well_constituents, qpcr_query)
        melt_graph = prepare_melt_graph(well_constituents, qpcr_query)
        copy_cnt_graph = prepare_copy_count_graph(well_constituents, qpcr_query)
        labchip_peaks = get_labchip_results_from_queryset(labchip_query)

        inst = cls.create(summary_table, master_table, amp_graph, melt_graph,
                          copy_cnt_graph, labchip_peaks)
        return inst


##TODO make below functions private

def get_qpcr_experiment_type(qpcr_query):
    """
    Retrieves experiment type info from first qpcr results record
    """
    qpcr_record = qpcr_query.first()
    experiment_type = qpcr_record.experiment.experiment_type

    return experiment_type


def get_well_constituents(qpcr_query):
    """
    Prepares data needed to make well constituents from qpcr query
    """
    qpcr_record = qpcr_query.first()
    experiment_id = qpcr_record.experiment.experiment_name
    qpcr_plate_id = qpcr_record.qpcr_plate_id
    qpcr_wells = qpcr_query.values_list('qpcr_well',flat=True)
    allocation_results = fetch_allocation_results(experiment_id)
    reagent_categories = fetch_reagent_categories()
    well_constituents = make_well_constituents(qpcr_plate_id, qpcr_wells,
                                               allocation_results,
                                               reagent_categories)

    return well_constituents




def get_master_table(well_constituents, qpcr_query, labchip_query):
    """
    Prepares a nested or vanilla master table from wellconstituents and
    queries based on experiment type
    """

    qpcr_record = qpcr_query.first()
    experiment_type = qpcr_record.experiment.experiment_type

    if experiment_type == 'nested':
        master_table=make_nested_master_table(well_constituents, qpcr_query,
                                              labchip_query)
    else:
        master_table=make_vanilla_master_table(well_constituents, qpcr_query,
                                               labchip_query)
    return master_table.rows

def create_summary_rows(master_table,qpcr_query):
    """
    prepares a summary table from master table
    """

    qpcr_record = qpcr_query.first()
    experiment_type = qpcr_record.experiment.experiment_type

    if experiment_type =='nested':
        summary_table = make_nested_summary_table(master_table)
    else:
        summary_table = make_vanilla_summary_table(master_table)

    return summary_table