import unittest
import os
from hardware.labchip_peak import LabChipPeakProcessor
from hardware.labchip_well_concentration import LabChipWellConcentration
from hardware.labchip_raw import LabChipRaw
class ExperitmentResultsTest(unittest.TestCase):

    def setUp(self):
      pass


    def test_excel_entry(self):
        root = os.path.abspath(os.getcwd())
        with open(root + r'/hardware/tests/data/2018-01-03_11-08'
                         r'-50_A81_20180103_A_PeakTable.csv', 'rb') as \
                file:
            labchip_parser = LabChipPeakProcessor()
            labchip_peak_data =labchip_parser.parse_labchip_peak_data(file)
            print(labchip_peak_data)

        with open(root + r'/hardware/tests/data/2018-01-03_11-08-50'
                         r'_A81_20180103_A_WellTable.csv', 'rb') as file:

            labchip_parser = LabChipWellConcentration()
            labchip_well_data =labchip_parser.parse_labchip_concentration_data(
                file)
            print(labchip_well_data)

        with open(root + r'/hardware/tests/data/2018-01-03_11-08'
                         r'-50_A81_20180103_A_RawTable.csv', 'rb') as file:

            labchip_parser = LabChipRaw()
            labchip_raw_data =labchip_parser.parse_labchip_raw_data(
                file)
            print(labchip_raw_data)