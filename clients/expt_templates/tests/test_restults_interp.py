
import os
import unittest
import numpy as np

from clients.utils import create_allocation_table
from hardware.step_one import StepOneExcel
from hardware.plates import create_plates_from_allocation_table

from clients.expt_templates.nested import build_constituents
from clients.expt_templates.results_interp import get_ct, get_mean_ct, \
    calc_delta_ct, get_ct_call
from clients.expt_templates.results_interp import get_tms, calc_mean_tm, \
    calc_tm_deltas
from clients.expt_templates.results_interp import is_ntc, get_ntc_wells
from clients.expt_templates.results_interp import get_product_labels_from_tms


class TestResultsInterp(unittest.TestCase):

    EXPT_NAME = '36'
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FILE = 'A81_E214_1_ID.xls'

    def setUp(self):

        allocation_table = create_allocation_table(TestResultsInterp.EXPT_NAME)
        plate_allocation_data = \
            create_plates_from_allocation_table(allocation_table)
        plate_id = TestResultsInterp.DATA_FILE.split('.')[0]
        self.plate_constituents = \
            build_constituents(plate_allocation_data[plate_id],
                               plate_allocation_data)

        f = os.path.join(TestResultsInterp.CURRENT_DIR, 'data',
                         TestResultsInterp.DATA_FILE)
        s1 = StepOneExcel(f)
        self.plate_results = s1.get_data_by_well()

    def test_ct_funcs(self):

        qpcr_data = self.plate_results['A01']
        ct = get_ct(qpcr_data)
        self.assertEqual(ct, 5.587069988250732)
        mean_ct = get_mean_ct(['A01', 'A02'], self.plate_results)
        self.assertEqual(mean_ct, 6.884355783462524)
        delta_ct = calc_delta_ct(ct, 0)
        self.assertEqual(delta_ct, -ct)
        call = get_ct_call(delta_ct)
        self.assertEqual(call, 'NEG')

    def test_tm_funcs(self):

        qpcr_data = self.plate_results['A01']
        tms = get_tms(qpcr_data)
        np.testing.assert_array_equal(tms, [79.1648941040039,
                                            74.78462219238281,
                                            62.46510314941406, np.nan])
        mean_tm = calc_mean_tm(['A01', 'A02'], self.plate_results)
        self.assertEqual(mean_tm, 77.11164093017578)
        tm_deltas = calc_tm_deltas(qpcr_data, 0)
        np.testing.assert_array_equal(tm_deltas, tms)

    def test_ntc_funcs(self):

        col1 = dict((w, wc) for w, wc in self.plate_constituents.items()
                    if w.endswith('01'))
        ntc_wells = get_ntc_wells(col1)
        for w, wc in ntc_wells.items():
            self.assertTrue(is_ntc(wc))

    def test_get_product_labels_from_tms(self):

        qpcr_data = self.plate_results['A01']
        tms = get_tms(qpcr_data)
        tm_deltas = calc_tm_deltas(qpcr_data, 0)
        spec, non_spec, pd = get_product_labels_from_tms(tms, tm_deltas, 0)
        self.assertFalse(spec)
        self.assertFalse(non_spec)
        self.assertTrue(pd)
