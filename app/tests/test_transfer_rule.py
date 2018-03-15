import unittest

from app.rules_engine.row_col_intersections import RowColIntersections
from app.rules_engine.transfer_rule import TransferRule
from app.rules_engine.transfer_rule import IncompatibleTransferError

class TransferRuleTest(unittest.TestCase):


    def test_compatible_combinations(self):

        # Make sure we can construct the compatible variants of source
        # and dest cells without raising an exception.

        # Single -> Anything
        TransferRule(
            'src_plate', 
            RowColIntersections((1,), (1,)),
            RowColIntersections((1,2,3), (4,5,6)),
            20, 'dilution')

        # Single row segment (4 cells), into rect spanning multiple rows, 
        # of width 4.
        TransferRule(
            'src_plate', 
            RowColIntersections((1,), (1,2,3,4)),
            RowColIntersections((1,2,3), (4,5,6,7)),
            20, 'dilution')

        # Single column segment (4 cells), into rect spanning multiple cols, 
        # of height 4.
        TransferRule(
            'src_plate', 
            RowColIntersections((1,2,3,4), (1,)),
            RowColIntersections((1,2,3,4), (4,5,6)),
            20, 'dilution')

        # Big rectangle 3 x 4 into another the same size.
        TransferRule(
            'src_plate', 
            RowColIntersections((1,2,3,), (4,5,6)),
            RowColIntersections((2,3,4), (5,6,7)),
            20, 'dilution')

    def test_incompatible_combinations(self):

        # Make sure the constructor raises IncompatibleTransferError when
        # incompatible combinations are used.

        # Source is not a rectangle but dest is..
        self.assertRaises(IncompatibleTransferError, TransferRule,
            'src_plate', 
            RowColIntersections((1,3), (1,)),
            RowColIntersections((1,2), (3,4)),
            20, 'dilution')

        # Dest is not a rectangle but source is..
        self.assertRaises(IncompatibleTransferError, TransferRule,
            'src_plate', 
            RowColIntersections((1,2), (3,4)),
            RowColIntersections((1,3), (1,)),
            20, 'dilution')

        # Row segment of length 2 into rect of width 3.
        self.assertRaises(IncompatibleTransferError, TransferRule,
            'src_plate', 
            RowColIntersections((1,), (3,4)),
            RowColIntersections((1,2,3), (2,3,4)),
            20, 'dilution')

        # Col segment of height 2 into rect of height 3.
        self.assertRaises(IncompatibleTransferError, TransferRule,
            'src_plate', 
            RowColIntersections((1,2), (1,)),
            RowColIntersections((2,3,4), (4,5,6)),
            20, 'dilution')

        # Rect size 3 x 4 into rect sized 2 x 3
        self.assertRaises(IncompatibleTransferError, TransferRule,
            'src_plate', 
            RowColIntersections((1,2,3), (1,2,3,4)),
            RowColIntersections((2,3), (4,5,6)),
            20, 'dilution')


if __name__ == '__main__':
    unittest.main()
