import unittest

from premixer import Premixer

class PremixerTest(unittest.TestCase):

    def test_simple_case(self):
        """
        This test uses capital letters for the mixture *items*.
        It sets up four buckets, each with a different mix.

        The mixtures are designed so that {AB} can be premixed for buckets
        {0,1,2,3}, while {C} can be premixed for buckets {0,1}.
        """

        # Exploiting Pythons constructor for making a set() of letters from
        # a string.
        buckets = [set(items) for items in ('ABCE', 'ABCF', 'ABDG', 'ABH')]
        premixer = Premixer(buckets)
        premixer.find_premixes()

        pm = premixer.premixes # Collect the results.

        # Should find exactly 2 premixes.
        self.assertEqual(len(pm), 2)

        # With the most-widely usable one first.
        premix, target_buckets = pm[0]
        self.assertEqual(premix, set('AB')) 
        self.assertEqual(target_buckets, [0, 1, 2, 3]) 

        # Followed by the one that targets fewer buckets.
        premix, target_buckets = pm[1]
        self.assertEqual(premix, set('C')) 
        self.assertEqual(target_buckets, [0, 1]) 


if __name__ == '__main__':
    unittest.main()
