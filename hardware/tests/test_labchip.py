
import unittest
import os

from hardware.labchip import LabChip, extract_bp_conc_pairs


class TestLabChip(unittest.TestCase):

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    PEAK = '2018-01-03_11-08-50_A81_20180103_A_PeakTable.csv'
    RAW = '2018-01-03_11-08-50_A81_20180103_A_RawTable.csv'
    WELL = '2018-01-03_11-08-50_A81_20180103_A_WellTable.csv'

    @classmethod
    def setUpClass(cls):

        peak = os.path.join(TestLabChip.CURRENT_DIR, 'data', TestLabChip.PEAK)
        raw = os.path.join(TestLabChip.CURRENT_DIR, 'data', TestLabChip.RAW)
        well = os.path.join(TestLabChip.CURRENT_DIR, 'data', TestLabChip.WELL)
        cls.lc_plate_data = LabChip(peak, raw, well).get_data_by_well()

    def test_peak_data(self):
        lc_well = self.lc_plate_data['A01']
        bp_conc = extract_bp_conc_pairs(lc_well)[0]
        self.assertEqual((11.268679019725, 0.146029612853322), bp_conc)
