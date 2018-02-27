from app.reagents.reagent_models import *
class SourceRowCol:
    """
    Contains the attributes of source ie plate number , row, column in case of transfer rule.
    """

    def __init__(self,plate_no,row,col):

        self.plate_no = plate_no
        self.row = row
        self.column = col

class PlacementInstructions:
    """
    Contain row ,col part of alloc rule
    """
    def __init__(self,row,col):
        self.row_range = row
        self.col_range = col

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
            end = int(self.col_range[2:])
            return [i for i in range(start, end + 1)]
        else:
            return [int(i) for i in self.col_range.split(',')]

class AllocRule:
    """
    *Alloc Rule* is short for "Allocation Rule".

    It encapsulates a recipe for repeating patterns of reagents to a
    rectangular region of an imaginary table.
    Has a Placement Instructions object which represents the target
    region of the table is defined in terms of row and column ranges.
    """
    def __init__(self,payload,row_range,col_range):

        #payload is a reagent reference
        self.payload = payload
        self.placement_instructions = PlacementInstructions(row_range,col_range)



    # todo consider moving this into __str or __repr
    def __str__(self):
        """
        E.g.
        'A  ATCC BAA-2355, Rows:A-H, Cols:1-12 50 x'
        """
        return ('A %s, %s,%s,%s' % (
            self.payload.name,
            'Rows:%s, Cols:%s' % (
                self.placement_instructions.row_range,
                self.placement_instructions.col_range
            ),
            self.payload.concentration.numerical_value,
            self.payload.concentration.preferred_units,
        ))


class TransferRule:

    def __init__(self,plate_no,row_range,col_range,dil):
        self.source_row_col = SourceRowCol(plate_no,row_range,col_range)
        self.placement_instructions = PlacementInstructions(row_range,col_range)
        self.dilution = dil
        self.payload = Reagent(self._make_reagent_name(),1,'x')


    def _make_reagent_name(self):
        return "Transfer from %s ,Row: %s,Col :%s"%(self.source_row_col.plate_no,self.source_row_col.row,self.source_row_col.column)
    def __str__(self):
        """
        E.g.
        'T P1 Rows:A-H, Cols:1-12 20 Dil'
        """
        return ('T P%s, %s,%s,%s' % (
            self.source_row_col.plate_no,
            'Rows:%s, Cols:%s' % (
                self.placement_instructions.row_range,
                self.placement_instructions.col_range
            ),
            self.payload.concentration.numerical_value,
            self.payload.concentration.preferred_units,
        ))