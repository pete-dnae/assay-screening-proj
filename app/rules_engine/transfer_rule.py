from app.rules_engine.row_col_intersections import RowColIntersections

class IncompatibleTransferError(Exception):
    pass

class TransferRule:
    """
    A transfer rule specifies rows and columns on an upstream *source* plate,
    and on a downstream *destination* plate. It refers to these rows and
    columns by holding a RowColIntersection object for the source and
    destination respectively.

    It also holds a dilution factor for the transfer.
    """


    def __init__(self, source_plate, source_cells, dest_cells, 
            conc, dilution_factor):
        """
        Provide the source and destination cells using one RowColIntersections
        object respectively.

        The class is only willing to accept some source->dest shape 
        combinations.  The constructor will raise an IncompatibleTransferError
        when the combination is incompatible.
        """
        self.source_plate = source_plate
        self.s_cells = source_cells
        self.d_cells = dest_cells
        self.conc = conc
        self.dilution_factor = dilution_factor
        if not self._compatible():
            raise IncompatibleTransferError()


    #-----------------------------------------------------------------------
    # Private below.
    #-----------------------------------------------------------------------

    def _compatible(self):
        """
        This class is only willing to accept some source->dest shape 
        combinations. This method reports if they are compatible.
        """

        s_shape, s_width, s_height = RowColIntersections(
                self.s_cells.rows, self.s_cells.cols).shape()
        d_shape, d_width, d_height = RowColIntersections(
                self.d_cells.rows, self.d_cells.cols).shape()

        # Single source can be tranferred to any shape destination.
        if s_shape == RowColIntersections.SINGLE:
            return True

        # Otherwise we required that BOTH the source and dest are rectangles.
        if s_shape != RowColIntersections.RECT:
            return False
        if d_shape != RowColIntersections.RECT:
            return False

        # From here on, we can depend on both source and dest being contiguous
        # rectangles.
    
        # If the source is a single row segment, then the destination rectangle
        # must have the same width.
        if s_height == 1:
            return d_width == s_width

        # If the source is a single column segment, then the destination 
        # rectangle must have the same height.
        if s_width == 1:
            return d_height == s_height

        # To reach here, both the source and dest are rectangles with both 
        # dimensions > 1. In wich case their sizes must match exactly.
        return (d_height == s_height) and (d_width == s_width)
