class AllocRule:
    """
    *Alloc Rule* is short for "Allocation Rule".

    It encapsulates a recipe for repeating patterns of reagents to a
    rectangular region of an imaginary table.
    The target region of the table is defined in terms of row and column
    ranges.
    """
    def __init__(self,payload,row_range,col_range):
        self.payload = payload
        self.row_range = row_range
        self.col_range = col_range

    def enumerate_applicable_rows(self):
        if "-" in self.row_range:
            start = ord(self.row_range[0]) - ord('A')
            end = ord(self.row_range[-1]) - ord('A')
            return [i for i in range(start, end + 1)]
        else:
            return self.row_range.split(',')

    def number_of_columns(self):
        return len(self.enumerate_column_indices())

    def enumerate_column_indices(self):
        if "-" in self.col_range:
            start = int(self.col_range[0])
            end = int(self.col_range[-1])
            return [i for i in range(start, end + 1)]
        else:
            return self.col_range.split(',')

    # todo consider moving this into __str or __repr
    def display_string(self):
        """
        E.g.
        'Strain, ATCC BAA-2355, Rows:A-H, Cols:1-12'
        """
        return ('%s, %s,%s' % (
            self.payload.name,
            self.payload.concentration.normalised_string_value,
            'Rows:%s, Cols:%s' % (
                self.row_range,
                self.col_range
            ),
        ))

