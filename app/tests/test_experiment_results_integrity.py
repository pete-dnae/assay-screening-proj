import unittest
from django.test import Client
from app.model_builders.make_test_experiment import make_test_experiment
from app.models.qpcr_results_model import QpcrResultsModel
from app.models.labchip_results_model import LabChipResultsModel

class ExperimentResultsIntegrity(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        make_test_experiment()

    def test_qpcr_data(self):

        qpcr_record = QpcrResultsModel.objects.get(experiment_id='A81_E214',
                                        qpcr_plate_id='A81_E214_1_ID',
                                        qpcr_well='E06')
        self.assertEquals(qpcr_record.cycle_threshold,14.30784034729)
        self.assertEquals(qpcr_record.temperatures,[84.7771148681641, None,
                                                    None, None])

    def test_labchip_data(self):

        labchip_record=LabChipResultsModel.objects.get(experiment_id='A81_E214',
                                        labchip_plate_id='20180103_A',
                                        labchip_well='P01',peak_name='Peak 2')
        self.assertEquals(labchip_record.size, 217.307692307692)
        self.assertEquals(labchip_record.concentration, 6.01032848141939)
        self.assertEquals(labchip_record.purity, 86.2324921728368)