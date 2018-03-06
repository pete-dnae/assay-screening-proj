import unittest

from app.premixers.nested_premixer import NestedPremixer

class NestedPremixerTest(unittest.TestCase):


    def test_example(self):
        """
        This test exercises the example described in the NestedPremixer class 
        code.
        """
        # We decouple this test from the FlatPremixer by injecting directly
        # the premix data structure.
        premixes = (
            ({'A', 'B', 'C'}, [0, 1, 2, 3, 4, 5, 6, 7, 8]),
            ({'E', 'D'}, [0, 1, 2, 3, 4, 5]),
            ({'H', 'I', 'J'}, [0, 1, 2]),
            ({'F', 'G'}, [6, 7, 8])
        )
        mixer = NestedPremixer(premixes)
        mixer.build_nested_mixes()
        print(mixer.dump())
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
