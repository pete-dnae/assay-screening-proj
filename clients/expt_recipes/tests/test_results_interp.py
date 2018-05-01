
import os.path as op
import unittest
import numpy as np


from clients.expt_recipes.well_constituents import WellConstituents
from hardware.qpcr import QpcrDataFile, get_ct, get_tms, calc_tm_deltas

from clients.expt_recipes.results_interpretation.qpcr import get_mean_ct, \
    calc_delta_ct, get_ct_call, calc_mean_tm, get_product_labels_from_tms
from clients.expt_recipes.results_interpretation.constituents import is_ntc, \
    get_ntc_wells

CURRENT_DIR = op.dirname(op.abspath(__file__))
NAV_ROOT = op.abspath(op.join(CURRENT_DIR, op.pardir, op.pardir, op.pardir))
DATA_DIR = op.join(NAV_ROOT, 'hardware', 'tests', 'data')
DATA_FILE = 'A81_E214_1_ID.xls'


class DummyWellConstituents(WellConstituents):

    def __init__(self):
        super().__init__()

    @classmethod
    def create(cls, templates):
        inst = cls()
        inst['templates'] = templates
        return inst


class TestResults(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        f = op.join(DATA_DIR, DATA_FILE)
        qpcr_data = QpcrDataFile(f)
        cls.plate_results = qpcr_data.get_data_by_well()

    def test_ct_funcs(self):

        qpcr_data = self.plate_results['A01']
        mean_ct = get_mean_ct(['A01', 'A02'], self.plate_results)
        self.assertEqual(mean_ct, 6.884355783462524)
        ct = get_ct(qpcr_data)
        delta_ct = calc_delta_ct(ct, 0)
        self.assertEqual(delta_ct, -ct)
        call = get_ct_call(delta_ct)
        self.assertEqual(call, 'NEG')

    def test_tm_funcs(self):

        qpcr_data = self.plate_results['A01']
        mean_tm = calc_mean_tm(['A01', 'A02'], self.plate_results)
        self.assertEqual(mean_tm, 77.11164093017578)
        tm_deltas = calc_tm_deltas(qpcr_data, 0)
        tms = get_tms(qpcr_data)
        np.testing.assert_array_equal(tm_deltas, tms)

    def test_get_product_labels_from_tms(self):

        qpcr_data = self.plate_results['A01']
        tms = get_tms(qpcr_data)
        tm_deltas = calc_tm_deltas(qpcr_data, 0)
        spec, non_spec, pd = get_product_labels_from_tms(tms, tm_deltas, 0)
        self.assertFalse(spec)
        self.assertFalse(non_spec)
        self.assertTrue(pd)


class TestAllocation(unittest.TestCase):

    def test_ntc_funcs(self):

        ntc = DummyWellConstituents.create(None)
        not_ntc = DummyWellConstituents.create('A lot of DNA')

        wells = {'A01': ntc, 'A02': not_ntc}
        ntc_wells = get_ntc_wells(wells)
        for w, wc in ntc_wells.items():
            self.assertTrue(is_ntc(wc))
