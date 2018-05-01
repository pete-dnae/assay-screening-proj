
import os
import unittest
import numpy as np

from clients.utils import create_allocation_table
from hardware.step_one import StepOneExcel
from hardware.plates import create_plates_from_allocation_table
from clients.expt_templates.nested import build_constituents, build_qpcr_datas


class TestNested(unittest.TestCase):

    EXPT_NAME = '36'
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FILE = 'A81_E214_1_ID.xls'

    def setUp(self):

        allocation_table = create_allocation_table(TestNested.EXPT_NAME)
        plate_allocation_data = \
            create_plates_from_allocation_table(allocation_table)
        plate_id = TestNested.DATA_FILE.split('.')[0]
        self.plate_constituents = \
            build_constituents(plate_allocation_data[plate_id],
                               plate_allocation_data)

        f = os.path.join(TestNested.CURRENT_DIR, 'data',
                         TestNested.DATA_FILE)
        s1 = StepOneExcel(f)
        self.plate_results = s1.get_data_by_well()

    def test_build_constituents(self):

        wc = self.plate_constituents['A01']

        assays = [{'concentration': 0.4,
                   'reagent_category': 'assay',
                   'reagent_name': 'Ca_rpb7_x.1_Cal04_Cal03',
                   'unit': 'uM'}]
        self.assertEqual(wc['assays'], assays)

        trans_assays = [{'concentration': 1.0,
                         'reagent_category': 'group assay',
                         'reagent_name': 'poolE1',
                         'unit': 'x'}]
        self.assertEqual(wc['transferred_assays'], trans_assays)

        templates = []
        self.assertEqual(wc['templates'], templates)

        trans_templates = []
        self.assertEqual(wc['transferred_templates'], trans_templates)

        human = []
        self.assertEqual(wc['human'], human)

        trans_human = []
        self.assertEqual(wc['transferred_human'], trans_human)

    def test_build_qpcr_datas(self):

        plate_results = build_qpcr_datas(self.plate_constituents,
                                         self.plate_results)
        wr = plate_results['A01']
        self.assertEqual(wr['Ct'], 5.587069988250732)
        self.assertEqual(wr['∆NTC_Ct'], 0.0)
        self.assertEqual(wr['Ct_Call'], 'NEG')
        self.assertEqual(wr['Tm1'], 79.1648941040039)
        self.assertEqual(wr['Tm2'], 74.78462219238281)
        self.assertEqual(wr['Tm3'], 62.46510314941406)
        self.assertTrue(np.isnan(wr['Tm4']))
        self.assertFalse(wr['Tm Specif'])
        self.assertFalse(wr['Tm NS'])
        self.assertTrue(wr['Tm PD'])
