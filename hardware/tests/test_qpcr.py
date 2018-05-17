

import unittest
import os
import numpy as np

from hardware.qpcr import QpcrDataFile, get_tms, get_ct


class TestQpcr(unittest.TestCase):

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FILE = 'A81_E214_1_ID.xls'

    @classmethod
    def setUpClass(cls):

        f = os.path.join(TestQpcr.CURRENT_DIR, 'data', TestQpcr.DATA_FILE)
        cls.qpcr_plate_data = QpcrDataFile(f).get_data_by_well()

    def test_tm_and_ct_extraction(self):

        qpcr_well_data = self.qpcr_plate_data['A01']
        ct = get_ct(qpcr_well_data)
        self.assertEqual(ct, 5.587069988250732)
        tms = get_tms(qpcr_well_data)
        np.testing.assert_array_equal(tms, [79.1648941040039,
                                            74.78462219238281,
                                            62.46510314941406, np.nan])
