from collections import defaultdict

"""
This module contains the closely allied classes: AllocRuleInterpreter and
AllocTable.
"""

class AllocTable():
    """
    A table-like data structure representing the grid of chambers on a 
    plate and for each cell, a list of what has been allocated to it.
    """

    def __init__(self, n_rows, n_cols):
        """
        This object's structure intends to make it easy to render the 
        table in an HTML <Table> element, by mimicing the <TR><TD> 
        nested sequences that are used in the HTML element.

        The table comprises an ordered sequence of rows.
        Each row is an ordered sequence of cells.
        Each cell is a dictionary keyed on strings like 'Strain'.

        The values against each of these keys is the string to display to
        represent that thing in the cell..

        Example for table row 2, column 3: (zero based indices).

            table[2][3]['PA-Primers'] = 'Efm_vanA_1.x_van05_van01'

        The constructor creates the data structure ready for the specified
        number of rows and columns, but nothing yet in the cell dictionaries.
        """
        self.rows = []
        for row_idx in range(n_rows):
            row = []
            self.rows.append(row)
            for col in range(n_cols):
                row.append({})


class AllocRuleInterpreter:
    """
    This class owns the business logic that knows how to interpret a sequence
    of AllocRule(s).

    Yoo construct it with a sequence of AllocRule(s), then can call its
    *interpret() method.

    It returns the *rows* attribute from the AllocTable it uses internally.
    """

    def __init__(self, rules):
        self._rules = rules
        self._n_rows = None
        self._n_cols = None
        self._table = None

    def interpret(self):
        # Treat there being zero rows as a special case, to avoid the
        # call to max() below receiving an empty sequence.
        if len(self._rules) == 0:
            self._table = AllocTable(0, 0)
            return self._table.rows
        # Drop in to the general case.

        # Work out how many rows and columns are implied by all the rules
        # used - taken together. I.e. the size of the resultant table
        # is calculated dynamically from the rules provided..
        self._n_rows = \
            1 + ord(max((r.end_row_letter for r in self._rules))) - ord('A')
        self._n_cols = max((r.end_column for r in self._rules))

        self._table = AllocTable(self._n_rows, self._n_cols)

        # Iterate to interpret each rule in turn. (Noting that later ones
        # overwrite earlier ones - by definition.
        for rule in self._rules:
            self._apply_rule_to_table(rule)
        return(self._table.rows)

    def _apply_rule_to_table(self, rule):
        """
        Apply the given AllocRule to the AllocTable under construction.
        """
        row_indices_range = rule.enumerate_applicable_rows()
        for row_index in row_indices_range:
            self._apply_rule_to_row(rule, row_index)

    def _apply_rule_to_row(self, rule, row_index):
        """
        Apply the given AllocRule to a single specified row in the table.
        """
        payload_items = rule.payload_items()
        # Have to use == (instead of 'is') to make equality test work 
        # between python string and Django models.CharField.
        if rule.pattern == 'Consecutive':
            self._consecutive(payload_items, rule, row_index)
        elif rule.pattern == 'In Blocks':
            self._in_blocks(payload_items, rule, row_index)

    def _consecutive(self, payload_items, rule, row_index):
        """
        Takes the items available in *payload_items* and distributes them
        in the given row, according to the *consecutive* pattern.

        I.e. place consecutive items from the payload into consecutive 
        columns, wrapping round the consecutive items if necessary to target
        all the columns mandated by the rule.
        """
        payload_item_index = 0
        for column_index in rule.enumerate_column_indices():
            self._set_item_in_table(
                row_index, column_index, rule.payload_type, 
                payload_items[payload_item_index])
            # Increment the payload item index using module division, to 
            # make it wrap back round the start when it goes off the end.
            payload_item_index = (payload_item_index + 1) % len(payload_items)

    def _in_blocks(self, payload_items, rule, row_index):
        """
        Takes the items available in *payload_items* and distributes them
        in the given row, according to the *in-blocks* pattern.

        I.e. divides up the column range cited by the rule into as many chunks
        as there are payload items, and then places the first payload item into
        all the columns in the first block. Then repeats the process with the
        second payload item and the second chunk of columns. Etc.
        """
        number_of_blocks = len(payload_items)
        if number_of_blocks == 0: # Avoid divide by zero.
            return
        size_of_blocks = int(rule.number_of_columns() / number_of_blocks)
        for block_index in range(number_of_blocks):
            payload_item = payload_items[block_index]
            start_column = \
                (rule.start_column - 1) + block_index * size_of_blocks
            end_column = (start_column - 1) + size_of_blocks
            for column_index in range(start_column, end_column + 1):
                self._set_item_in_table(
                    row_index, column_index, rule.payload_type, 
                    payload_item)

    def _set_item_in_table(self, row_index, column_index, payload_type,
            payload_item):
        # Note this might be overwriting a previous value because later
        # rules overwrite the results from earlier rules, by definition.

        t = payload_type.type
        self._table.rows[row_index][column_index][t] = payload_item


                


