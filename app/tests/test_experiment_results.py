import unittest
from django.test import Client
from app.models import QpcrResultsModel
from app.model_builders.make_test_experiment import make_test_experiment
from app.experiment_results.qpcr_well_aggregation import \
    get_well_constituents,get_master_table ,create_summary_rows,get_labchip_query
class ExperimentResults(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     make_test_experiment()



    def test_experiment_summary(self):
        qpcr_query = QpcrResultsModel.objects.filter(
            experiment_id='A81_E214', qpcr_plate_id="A81_E214_1_ID",
            reagentwelllookupmodel__reagent_id="Ab_pgaD_x.10_Aba38_Aba42")
        well_constituents = get_well_constituents(qpcr_query)
        labchip_query = get_labchip_query(qpcr_query)
        master_table = get_master_table(well_constituents,qpcr_query,labchip_query)
        print(well_constituents)

