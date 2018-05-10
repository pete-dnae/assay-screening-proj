
import os.path as op
import unittest
import numpy as np


from clients.expt_recipes.well_constituents import WellConstituents
from hardware.qpcr import QpcrDataFile, get_ct, get_tms, calc_tm_deltas, \
    get_mean_ct, calc_mean_tm

from clients.expt_recipes.interp.qpcr import calc_delta_ct, get_ct_call, \
    get_product_labels_from_tms
from clients.expt_recipes.interp.constituents import is_ntc, \
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
        qpcr_data_file = QpcrDataFile(f)
        cls.plate_results = qpcr_data_file.get_data_by_well()
        cls.qpcr_data = cls.plate_results['A01']

    def test_ct_funcs(self):

        qpcr_datas = [self.plate_results[w] for w in ['A01', 'A02']]
        mean_ct = get_mean_ct(qpcr_datas)
        self.assertEqual(mean_ct, 6.884355783462524)
        ct = get_ct(self.qpcr_data)
        delta_ct = calc_delta_ct(ct, 0)
        self.assertEqual(delta_ct, -ct)
        call = get_ct_call(delta_ct)
        self.assertEqual(call, 'NEG')

    def test_tm_funcs(self):
        qpcr_datas = [self.plate_results[w] for w in ['A01', 'A02']]
        mean_tm = calc_mean_tm(qpcr_datas)
        self.assertEqual(mean_tm, 77.11164093017578)
        tm_deltas = calc_tm_deltas(self.qpcr_data, 0)
        tms = get_tms(self.qpcr_data)
        np.testing.assert_array_equal(tm_deltas, tms)

    def test_get_product_labels_from_tms(self):

        tms = get_tms(self.qpcr_data)
        tm_deltas = calc_tm_deltas(self.qpcr_data, 0)
        spec, non_spec, pd = get_product_labels_from_tms(tms, tm_deltas, 0)
        self.assertEqual([spec, non_spec, pd], [False, False, True])


class TestAllocation(unittest.TestCase):

    def test_ntc_funcs(self):

        ntc = DummyWellConstituents.create(None)
        not_ntc = DummyWellConstituents.create('A lot of DNA')
        wells = {'A01': ntc, 'A02': not_ntc}
        ntc_wells = get_ntc_wells(wells)
        for w, wc in ntc_wells.items():
            self.assertTrue(is_ntc(wc))
