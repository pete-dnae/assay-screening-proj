import unittest

from app.premixers.flat_premixer import FlatPremixer

class FlatPremixerTest(unittest.TestCase):


    def test_example(self):
        """
        This test exercises the example described in the FlatPremixer class 
        code.
        """
        buckets = []

        buckets.append(set('ABCDEHIJK'))
        buckets.append(set('ABCDEHIJL'))
        buckets.append(set('ABCDEHIJM'))
        buckets.append(set('ABCDEN'))
        buckets.append(set('ABCDEO'))
        buckets.append(set('ABCDEP'))
        buckets.append(set('ABCFGQ'))
        buckets.append(set('ABCFGR'))
        buckets.append(set('ABCFGS'))

        mixer = FlatPremixer(buckets)
        mixer.find_premixes()

        self.assertEqual(len(mixer.premixes), 4)


        self.assertIn(({'A', 'B', 'C'}, [0, 1, 2, 3, 4, 5, 6, 7, 8]),
            mixer.premixes)

        self.assertIn(({'E', 'D'}, [0, 1, 2, 3, 4, 5]),
            mixer.premixes)

        self.assertIn(({'H', 'I', 'J'}, [0, 1, 2]),
            mixer.premixes)

        self.assertIn(({'F', 'G'}, [6, 7, 8]),
            mixer.premixes)



if __name__ == '__main__':
    unittest.main()
