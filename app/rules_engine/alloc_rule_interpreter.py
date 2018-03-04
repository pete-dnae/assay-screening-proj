from collections import defaultdict
import re
"""
This module contains the closely allied classes: AllocRuleInterpreter,AllocTable and RuleParser.
"""

class AllocationResults():
    """
    A table-like data structure representing the grid of chambers on a 
    plate and for each cell, a list of what has been allocated to it.
    """

    def __init__(self):
        """
        This object's structure intends to make it easy to render the 
        table in an HTML <Table> element, by minimicing the <TR><TD>
        nested sequences that are used in the HTML element.

        The table comprises an dictionary of rows.
        Each row is an ordered sequence of cells.

        The values against each of these keys is the list of reagent objects present in that cell

        Example for table row B, column 3: (zero based indices).

            table[B][3]['PA-Primers'] = [reagent,reagent,reagent]

        The constructor creates the data structure ready for the specified
        number of rows and columns, but nothing yet in the cell dictionaries.
        """
        self.rows = defaultdict(dict)

    def add(self, row, col, reagent):
        self.rows[row].setdefault(col, []).append(reagent)

class AllocRuleInterpreter:
    """
    This class owns the business logic that knows how to interpret a sequence
    of AllocRule(s).

    Yoo construct it with a sequence of AllocRule(s), then can call its
    *interpret()* method.

    It returns the *rows* attribute from the AllocTable it uses internally.
    """

    def __init__(self, rules):
        self._rules = rules
        self._table = None

    def interpret(self):
        # Treat there being zero rows as a special case, to avoid the
        # call to max() below receiving an empty sequence.
        self._table = AllocationResults()
        if len(self._rules) == 0:
            return self._table.rows
        # Drop in to the general case.

        # Iterate to interpret each rule in turn. (Noting that later ones
        # overwrite earlier ones - by definition.
        for i,rule in self._rules.items():
            self._apply_rule_to_table(rule)
        return(self._table)

    def _apply_rule_to_table(self, rule):
        """
        Apply the given AllocRule to the AllocTable under construction.
        """
        row_indices_range = rule.placement_instructions.enumerate_applicable_rows()
        for row_index in row_indices_range:
            self._apply_rule_to_row(rule, row_index)

    def _apply_rule_to_row(self, rule, row_index):
        """
        Apply the given AllocRule to a single specified row in the table.
        """
        self._fill_row(rule.payload, rule, row_index)


    def _fill_row(self, payload_item, rule, row_index):
        """
        Takes the item available in *payload_item* and fills them in a 
        given range.
        """
        for column_index in rule.placement_instructions.enumerate_column_indices():
            self._set_item_in_table(
                row_index, column_index,
                payload_item)

    def _set_item_in_table(self, row_index, column_index,
            payload_item):
        # Note this might be overwriting a previous value because later
        # rules overwrite the results from earlier rules, by definition.

        row_alph = chr(65 + row_index)
        self._table.add(row_alph,column_index,payload_item)


