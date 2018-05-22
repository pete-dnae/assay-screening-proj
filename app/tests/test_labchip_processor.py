import unittest
import os
from app.models.experiment_model import ExperimentModel
from app.experiment_results.labchip_results_processor import LabChipResultsProcessor
class ExperitmentResultsTest(unittest.TestCase):

    def setUp(self):
      pass


    def test_excel_entry(self):
        root = os.path.abspath(os.getcwd())
        with open(root + r'/hardware/tests/data/2018-01-03_11-08'
                         r'-50_A81_20180103_A_PeakTable.csv', 'rb') as \
                file:
            labchip_processor = LabChipResultsProcessor(
                plate_name='20180103_A',experiment_name='A81_E214')
            labchip_results = labchip_processor.parse_labchip_file(file)
            print(labchip_results)


