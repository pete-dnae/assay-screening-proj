class RowColIntersections():
    """
    This class stores a list of some rows and columns that you specify and can 
    provide you with a list of all the cells thus formed by their intersections, 
    along with whether this comprises a contiguous rectangular region or not.

    CAUTION

    The vast majority of the code in the rest of the rules subsystem always
    specifies rows and columns in data structures and in positional arguments
    to functions, and in data payloads, by specifying column then row. E.g
    (2,3) usually means column 2, row 3. The exception is this
    RowColumnIntersection class, which reverses this convention in order to
    match up with the name of the class.
    """

    SINGLE = 1
    RECT = 2
    AMORPHOUS = 3

    def __init__(self, rows, cols):
        # We sort these on the way in to make tests for contiguous easier.
        self.rows = sorted(rows)
        self.cols = sorted(cols)

    def all_cells(self):
        """
        Returns a sequence like this: ((row, col), (row, col), ...))
        """
        res = []
        for row in self.rows:
            for col in self.cols:
                res.append((row, col))
        return res

    def minimums(self):
        """
        Returns the minimum row number followed by the minimum
        column number.
        """
        # Take advantage of them being sorted already.
        return ((self.rows[0], self.cols[0]))

    def shape(self):
        """
        Returns one of SINGLE, RECT, AMORPHOUS. Followed by width and height.
        Width and height are undefined for AMORPHOUS
        """
        # Return early for the single-cell singularity to make the other 
        # tests simpler.
        if (len(self.rows)) == 1 and (len(self.cols) == 1):
            return RowColIntersections.SINGLE, 1, 1

        # If either rows or columns have discontinuities, we must conclude
        # amorphous.
        row_continuity = self._assess_continuity(self.rows)
        col_continuity = self._assess_continuity(self.cols)

        if (row_continuity == False) or (col_continuity == False):
            return RowColIntersections.AMORPHOUS, None, None

        # To reach here, it must be a rectangular region.
        width = len(self.cols)
        height = len(self.rows)
        return RowColIntersections.RECT, width, height
        

    def _assess_continuity(self, a_sequence):
        """
        Returns True if the sequence contains integers which taken together,
        form a contiguous sequence.
        """
        smallest = min(a_sequence)
        largest = max(a_sequence)
        required_set = set([i for i in range(smallest, largest + 1)])
        presented_set = set(a_sequence)
        return required_set == presented_set
