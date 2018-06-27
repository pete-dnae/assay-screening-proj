import unittest
from pdb import set_trace as st

from app.model_builders.make_ref_exp import ReferenceExperiment
from app.view_helpers import ViewHelpers


class ViewHelperTest(unittest.TestCase):

    def setUp(self):
        experiment = ReferenceExperiment()
        experiment.create()

    #-----------------------------------------------------------------------
    def test_all_allowed_names(self):
        all_names = ViewHelpers.all_allowed_names()

        reagents_and_groups = all_names['reagents_and_groups']
        # Have to check against only those created by the reference experiment,
        # because there can be others mixed in that are created by other
        # units tests.

        for name in (
                '(Eco)-ATCC-BAA-2355',
                '(Eco)-ATCC-BAA-9999',
                'Ec_uidA_6.x_Eco63_Eco60',
                'Efs_cpn60_1.x_Efs04_Efs01',
                'Efs_vanB_1.x_van10_van06',
                'Pool_1',
                'Titanium-Taq'):
            self.assertTrue(name in reagents_and_groups)

        self.assertEqual(all_names['units'], ['%','M/uL','cp','cp/ul',
                                              'dilution','mM','mg/ml','nM',
                                              'ng','ng/ul','uM','ug/ml','x'])
