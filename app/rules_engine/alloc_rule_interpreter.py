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
        table in an HTML <Table> element, by minimicing the <TR><TD>
        nested sequences that are used in the HTML element.

        The table comprises an dictionary of rows.
        Each row is an ordered sequence of cells.
        Each cell is a dictionary keyed on strings like 'Strain'.

        The values against each of these keys is the string to display to
        represent that thing in the cell..

        Example for table row B, column 3: (zero based indices).

            table[B][3]['PA-Primers'] = 'Efm_vanA_1.x_van05_van01'

        The constructor creates the data structure ready for the specified
        number of rows and columns, but nothing yet in the cell dictionaries.
        """
        self.rows = {}
        for row_idx in range(n_rows):
            row = []
            row_alph = chr(65+row_idx)
            self.rows[row_alph]=row
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
        payload_item = rule.payload_item()
        self._fill_row(payload_item, rule, row_index)


    def _fill_row(self, payload_item, rule, row_index):
        """
        Takes the item available in *payload_item* and fills them in a given range
        """
        for column_index in range(rule.start_column-1,rule.end_column):
            self._set_item_in_table(
                row_index, column_index, rule.payload_type,
                payload_item)

    def _set_item_in_table(self, row_index, column_index, payload_type,
            payload_item):
        # Note this might be overwriting a previous value because later
        # rules overwrite the results from earlier rules, by definition.
        row_alph = chr(65 + row_index)
        self._table.rows[row_alph][column_index][payload_type] = payload_item


                


