import unittest

from app.premixers.premixer import Premixer
from app.models.reagent_models import *
from app.model_builders.make_ref_exp import ReferenceExperiment
from app.model_builders.finders import Finders
class PremixerTest(unittest.TestCase):


    def setUp(self):
        self._create_concentrations()
        self._create_buffer_reagents()

    def test_simple_case(self):
        """
        This test uses capital letters for the mixture *items*.
        It sets up four buckets, each with a different mix.

        The mixtures are designed so that {AB} can be premixed for buckets
        {0,1,2,3}, while {C} can be premixed for buckets {0,1}.
        """

        # Exploiting Pythons constructor for making a set() of letters from
        # a string.
        finder = Finders()


        setA = {finder._reagent(Reagent.make_hash('BSA',Concentration.value_from_quotient(20, 1))),
                finder._reagent(Reagent.make_hash('SYBRgreen', Concentration.value_from_quotient(100,0.32))),
                finder._reagent(Reagent.make_hash('Triton', Concentration.value_from_quotient(10,0.04))),
                finder._reagent(Reagent.make_hash('Titanium Taq', Concentration.value_from_quotient(50,1.3)))}

        setB= {finder._reagent(Reagent.make_hash('BSA',Concentration.value_from_quotient(20, 1))),
               finder._reagent(Reagent.make_hash('Triton', Concentration.value_from_quotient(10,0.04))),
               finder._reagent(Reagent.make_hash('SYBRgreen', Concentration.value_from_quotient(100,0.32))),
               finder._reagent(Reagent.make_hash('Titanium Taq', Concentration.value_from_quotient(50,1.3)))}

        setC={finder._reagent(Reagent.make_hash('BSA',Concentration.value_from_quotient(20, 1))),
              finder._reagent(Reagent.make_hash('Triton', Concentration.value_from_quotient(10, 0.04))),
              finder._reagent(Reagent.make_hash('Titanium Taq', Concentration.value_from_quotient(50,1.0))),
              }


        buckets = [setA,setB,setC]
        premixer = Premixer(buckets)
        premixer.find_premixes()

        pm = premixer.premixes # Collect the results.

        # Should find exactly 2 premixes.
        self.assertEqual(len(pm), 2)

        # With the most-widely usable one first.
        premix, target_buckets = pm[0]
        self.assertEqual(premix, {finder._reagent(Reagent.make_hash('BSA',Concentration.value_from_quotient(20, 1))),
                                  finder._reagent(Reagent.make_hash('Triton', Concentration.value_from_quotient(10, 0.04)))})
        self.assertEqual(target_buckets, [0, 1, 2])

        # Followed by the one that targets fewer buckets.
        premix, target_buckets = pm[1]
        self.assertEqual(premix, {finder._reagent(Reagent.make_hash('Titanium Taq', Concentration.value_from_quotient(50,1.3))),
                                  finder._reagent(Reagent.make_hash('SYBRgreen', Concentration.value_from_quotient(100,0.32)))})
        self.assertEqual(target_buckets, [0, 1])


    def _create_concentrations(self):
        for denom, numerator, pref_units in (
                (1, 1, 'X'),
                (10, 0.13, 'X'),
                (10, 0.2, 'mM'),
                (10, 0.04, '%'),
                (20, 1, 'mg/ml'),
                (25, 2.06, 'mM'),
                (50, 1.0, 'x'),
                (50, 1.3, 'x'),
                (100, 0.32, 'X'),
                (100, 1, 'mM'),
                (1000, 48, 'mM')):
            Concentration.make(numerator / float(denom), pref_units)



    def _create_buffer_reagents(self):
        finder = Finders()
        Reagent.make('BSA', '-', finder._conc_rat(20, 1, 'mg/ml'))
        Reagent.make('DNA Free Water', '22884100', finder._conc_rat(1, 1, 'X'))
        Reagent.make('dNTPs', '-', finder._conc_rat(10, 0.2, 'mM'))
        Reagent.make('KCl', '-', finder._conc_rat(1000, 48, 'mM'))
        Reagent.make('KOH', '-', finder._conc_rat(100, 1, 'mM'))
        Reagent.make('MgCl2', '449890', finder._conc_rat(25, 2.06, 'mM'))
        Reagent.make('Titanium PCR Buffer', '1602046A',
                     finder._conc_rat(10, 0.13, 'X'))
        Reagent.make('SYBRgreen', '-', finder._conc_rat(100, 0.32, 'X'))
        Reagent.make('Titanium Taq', '1607230A', finder._conc_rat(50, 1.0, 'x'))
        Reagent.make('Titanium Taq', '1607230A', finder._conc_rat(50, 1.3, 'x'))
        Reagent.make('Triton', '-', finder._conc_rat(10, 0.04, '%'))



if __name__ == '__main__':
    unittest.main()
