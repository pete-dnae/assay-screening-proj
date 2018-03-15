from pdb import set_trace as st

from app.rules_engine.row_col_intersections import RowColIntersections

class IncompatibleTransferError(Exception):
    pass

class TransferRule:
    """
    A transfer rule specifies rows and columns on an upstream *source* plate,
    and on a downstream *destination* plate. It refers to these rows and
    columns by holding a RowColIntersection object for the source and
    for the destination respectively. It also holds a dilution factor for the 
    transfer.

    The shape made by the rows and columns of the source does not have to match
    exactly that made by the destination. But only some combinations are
    allowed. Namely:

    rectangle           -> exactly matching rectangle
    horizontal strip    -> rectangle of matching width but any height (incl. 1)
    vertical strip      -> rectangle of matching height but any width (incl. 1)
    single cell         -> anything you like

    The constructor throws IncompatibleTransferError when your combination does
    not satisfy these constraints.

    After successful construction you can access a mapping for which source
    cells provides the source for any given destination cell in self.mapping.

    self.mapping works like this: using (d) for destination and (s) for source.

            self.mapping[d_row][d_col] = (s_row, s_col)
    """


    def __init__(self, source_plate, source_cells, 
            dest_cells, dilution_factor):
        """
        Provide the source and destination cells using one RowColIntersections
        object respectively. The constructor will raise an 
        IncompatibleTransferError when the combination is incompatible.
        """
        self.source_plate = source_plate
        self.s_cells = source_cells
        self.d_cells = dest_cells
        self.dilution_factor = dilution_factor
        self.mapping = {}
        self._populate_mapping() # Can raise IncompatibleTransferError


    #-----------------------------------------------------------------------
    # Private below.
    #-----------------------------------------------------------------------

    def _populate_mapping(self):
        """
        Works out what shape the source cells make and what shape the
        destination cells shape makes. Then (provided they are compatible),
        stores a mapping between them in self.mapping. Raises
        IncompatibleTransferError if they are not compatible.
        """

        s_cells = RowColIntersections(
                self.s_cells.rows, self.s_cells.cols)
        d_cells = RowColIntersections(
                self.d_cells.rows, self.d_cells.cols)

        s_shape, s_width, s_height = s_cells.shape()
        d_shape, d_width, d_height = d_cells.shape()

        # Single source can be tranferred to any shape destination.
        if s_shape == RowColIntersections.SINGLE:
            self._populate_as_single_to_many(s_cells, d_cells)
            return

        # Otherwise we required that BOTH the source and dest are rectangles.
        if s_shape != RowColIntersections.RECT:
            raise IncompatibleTransferError()
        if d_shape != RowColIntersections.RECT:
            raise IncompatibleTransferError()

        # From here on, we can depend on both source and dest being contiguous
        # rectangles, but this include either a width or height of one.
    
        # If the source is a single row segment, then the destination rectangle
        # must have the same width.
        if s_height == 1:
            if d_width != s_width:
                raise IncompatibleTransferError()
            self._populate_as_row_seg_to_rect(s_cells, d_cells)
            return

        # If the source is a single column segment, then the destination 
        # rectangle must have the same height.
        if s_width == 1:
            if d_height != s_height:
                raise IncompatibleTransferError()
            self._populate_as_col_seg_to_rect(s_cells, d_cells)
            return

        # To reach here, both the source and dest are rectangles with both 
        # dimensions > 1. In wich case their sizes must match exactly.
        if (d_height != s_height) or (d_width != s_width):
            raise IncompatibleTransferError()
        self._populate_as_rect_to_rect(s_cells, d_cells)
        return

    def _populate_as_single_to_many(self, s_cells, d_cells):
        """
        Populate self.mapping in the prior knowledge that the source cells 
        is just a single cell, and the destination cells can be anything.
        """
        s_row, s_col = s_cells.all_cells()[0]
        for d_row, d_col in d_cells.all_cells():
            columns = self.mapping.setdefault(d_row, {})
            columns[d_col] = (s_row, s_col)

    def _populate_as_row_seg_to_rect(self, s_cells, d_cells):
        """
        Populate self.mapping in the prior knowledge that the source cells 
        comprise a horizontal strip, and the destination cells form a 
        rectangle of the same width.
        """
        s_min_row, s_min_col = s_cells.minimums()
        d_min_row, d_min_col = d_cells.minimums()
        # Populate the mapping for all the destination cells
        for d_row, d_col in d_cells.all_cells():
            columns = self.mapping.setdefault(d_row, {})
            columns[d_col] = (s_min_row, s_min_col + d_col - d_min_col)

    def _populate_as_col_seg_to_rect(self, s_cells, d_cells):
        """
        Populate self.mapping in the prior knowledge that the source cells 
        comprise a vertical strip, and the destination cells form a 
        rectangle of the same height.
        """
        s_min_row, s_min_col = s_cells.minimums()
        d_min_row, d_min_col = d_cells.minimums()
        # Populate the mapping for all the destination cells
        for d_row, d_col in d_cells.all_cells():
            columns = self.mapping.setdefault(d_row, {})
            columns[d_col] = (s_min_row + d_row - d_min_row, s_min_col)
            

    def _populate_as_rect_to_rect(self, s_cells, d_cells):
        """
        Populate self.mapping in the prior knowledge that the source cells 
        is a full rect, and the destination cells form a rectangle of
        exactly the same shape..
        """
        # Populate the mapping for all the destination cells
        s_min_row, s_min_col = s_cells.minimums()
        d_min_row, d_min_col = d_cells.minimums()
        for d_row, d_col in d_cells.all_cells():
            columns = self.mapping.setdefault(d_row, {})
            columns[d_col] = (s_min_row + d_row - d_min_row, 
                    s_min_col + d_col - d_min_col)






