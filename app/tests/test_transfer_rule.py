import unittest

from app.rules_engine.row_col_intersections import RowColIntersections
from app.rules_engine.transfer_rule import TransferRule
from app.rules_engine.transfer_rule import IncompatibleTransferError

class TransferRuleTest(unittest.TestCase):


    def test_compatible_combinations(self):

        # Make sure we can construct the compatible variants of source
        # and dest cells without raising an exception.

        # Single -> Anything
        t = TransferRule(
            'src_plate', 
            RowColIntersections((1,), (1,)),
            RowColIntersections((1,2,3), (4,5,6)),
            20)
        # Check random sample of dest->source mappings produced. Should all be 
        # mappings back to source cell (1,1) in this case.
        m = t.mapping
        self.assertEqual(m[2][6], (1, 1))

        # Single row segment (4 cells), into rect spanning multiple rows, 
        # of width 4.
        t = TransferRule(
            'src_plate', 
            RowColIntersections((1,), (1,2,3,4)),
            RowColIntersections((1,2,3), (4,5,6,7)),
            20)
        # TLHC of destination rect should map back to start of source strip.
        # TRHC of destination rect should map back to end of source strip.
        # BRHC of destination rect should map back to end of source strip.
        m = t.mapping
        self.assertEqual(m[1][4], (1, 1))
        self.assertEqual(m[1][7], (1, 4))
        self.assertEqual(m[3][7], (1, 4))

        # Single column segment (4 cells), into rect spanning multiple cols, 
        # of height 4.
        t = TransferRule(
            'src_plate', 
            RowColIntersections((1,2,3,4), (1,)),
            RowColIntersections((1,2,3,4), (4,5,6)),
            20)
        m = t.mapping
        # TLHC of destination rect should map back to start of source strip.
        # TRHC of destination rect should map back to start of source strip.
        # BRHC of destination rect should map back to end of source strip.
        m = t.mapping
        self.assertEqual(m[1][4], (1, 1))
        self.assertEqual(m[1][6], (1, 1))
        self.assertEqual(m[4][6], (4, 1))

        # Big rectangle 3 x 4 into another the same size.
        t = TransferRule(
            'src_plate', 
            RowColIntersections((1,2,3,), (4,5,6)),
            RowColIntersections((2,3,4), (5,6,7)),
            20)
        m = t.mapping
        # Arbitrary sample in the middle somewhere
        self.assertEqual(m[3][6], (2, 5))

    def test_incompatible_combinations(self):

        # Make sure the constructor raises IncompatibleTransferError when
        # incompatible combinations are used.

        # Source is not a rectangle but dest is..
        self.assertRaises(IncompatibleTransferError, TransferRule,
            'src_plate', 
            RowColIntersections((1,3), (1,)),
            RowColIntersections((1,2), (3,4)),
            20)

        # Dest is not a rectangle but source is..
        self.assertRaises(IncompatibleTransferError, TransferRule,
            'src_plate', 
            RowColIntersections((1,2), (3,4)),
            RowColIntersections((1,3), (1,)),
            20)

        # Row segment of length 2 into rect of width 3.
        self.assertRaises(IncompatibleTransferError, TransferRule,
            'src_plate', 
            RowColIntersections((1,), (3,4)),
            RowColIntersections((1,2,3), (2,3,4)),
            20)

        # Col segment of height 2 into rect of height 3.
        self.assertRaises(IncompatibleTransferError, TransferRule,
            'src_plate', 
            RowColIntersections((1,2), (1,)),
            RowColIntersections((2,3,4), (4,5,6)),
            20)

        # Rect size 3 x 4 into rect sized 2 x 3
        self.assertRaises(IncompatibleTransferError, TransferRule,
            'src_plate', 
            RowColIntersections((1,2,3), (1,2,3,4)),
            RowColIntersections((2,3), (4,5,6)),
            20)


if __name__ == '__main__':
    unittest.main()
