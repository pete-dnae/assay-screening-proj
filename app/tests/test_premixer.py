import unittest

from app.premixers.premixer import Premixer

class PremixerTest(unittest.TestCase):


    def test_example(self):
        """
        This test exercises the example described in the Premixer class code.
        """
        buckets = []

        buckets.append(set('ABCDGHI'))
        buckets.append(set('ABCDGHJ'))
        buckets.append(set('ABCDK'))
        buckets.append(set('ABEFL'))
        buckets.append(set('ABEFM'))

        premixer = Premixer(buckets)
        premixer.find_premixes()

        pm = premixer.premixes # Collect the results.


if __name__ == '__main__':
    unittest.main()
