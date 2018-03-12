import unittest

from app.rules_engine.row_col_intersections import RowColIntersections

class RowColIntersectionTest(unittest.TestCase):


    def test_can_detect_single(self):
        rows = (1,)
        cols = (3,)
        inter = RowColIntersections(rows, cols)
        all_cells = inter.all_cells()
        self.assertTrue(len(all_cells), 1)
        self.assertEqual(all_cells[0], (1,3))
        shape, w, h = inter.shape()
        self.assertEqual(shape, RowColIntersections.SINGLE)
        self.assertEqual(w, 1)
        self.assertEqual(h, 1)

    def test_correctly_detects_big_fat_rectangle(self):
        rows = (1,3,2) # Deliberately in jumbled wrong order.
        cols = (6,7,8,9)
        inter = RowColIntersections(rows, cols)
        all_cells = inter.all_cells()
        self.assertTrue(len(all_cells), 12)
        self.assertEqual(all_cells[0], (1,6))
        self.assertEqual(all_cells[11], (3,9))
        shape, w, h = inter.shape()
        self.assertEqual(shape, RowColIntersections.RECT)
        self.assertEqual(w, 4)
        self.assertEqual(h, 3)

    def test_correctly_detects_horiz_strip_rectangle(self):
        rows = (1,)
        cols = (6,7,8,9)
        inter = RowColIntersections(rows, cols)
        all_cells = inter.all_cells()
        self.assertTrue(len(all_cells), 4)
        self.assertEqual(all_cells[0], (1,6))
        self.assertEqual(all_cells[3], (1,9))
        shape, w, h = inter.shape()
        self.assertEqual(shape, RowColIntersections.RECT)
        self.assertEqual(w, 4)
        self.assertEqual(h, 1)

    def test_correctly_detects_vert_strip_rectangle(self):
        rows = (6,7,8,9)
        cols = (1,)
        inter = RowColIntersections(rows, cols)
        all_cells = inter.all_cells()
        self.assertTrue(len(all_cells), 4)
        self.assertEqual(all_cells[0], (6,1))
        self.assertEqual(all_cells[3], (9,1))
        shape, w, h = inter.shape()
        self.assertEqual(shape, RowColIntersections.RECT)
        self.assertEqual(w, 1)
        self.assertEqual(h, 4)

    def test_correctly_detects_amorphous(self):
        rows = (6,8)
        cols = (1,)
        inter = RowColIntersections(rows, cols)
        all_cells = inter.all_cells()
        self.assertTrue(len(all_cells), 2)
        self.assertEqual(all_cells[0], (6,1))
        self.assertEqual(all_cells[1], (8,1))
        shape, w, h = inter.shape()
        self.assertEqual(shape, RowColIntersections.AMORPHOUS)
        self.assertIsNone(w)
        self.assertIsNone(h)

if __name__ == '__main__':
    unittest.main()
