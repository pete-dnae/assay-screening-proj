from collections import defaultdict


class AllocRuleInterpreter:

    def __init__(self, rules):
        self._rules = rules
        self._n_rows = None
        self._n_cols = None
        self._table = None

    def interpret(self):
        self._n_rows = \
            1 + ord(max((r.end_row_letter for r in self._rules))) - ord('A')
        self._n_cols = max((r.end_column for r in self._rules))

        self._table = AllocTable(self._n_rows, self._n_cols)

        for rule in self._rules:
            self._apply_rule_to_table(rule)
        return(self._table.rows)

    def _apply_rule_to_table(self, rule):
        print('XXXXX payload type: <%s>' % rule.payload_type)
        row_indices_range = rule.enumerate_applicable_rows()
        for row_index in row_indices_range:
            self._apply_rule_to_row(rule, row_index)

    def _apply_rule_to_row(self, rule, row_index):
        payload_items = rule.payload_items()
        # Have to use == (instead of 'is') to make equality test work 
        # between python string and Django models.CharField.
        if rule.pattern == 'Consecutive':
            self._consecutive(payload_items, rule, row_index)
        elif rule.pattern == 'In Blocks':
            self._in_blocks(payload_items, rule, row_index)

    def _consecutive(self, payload_items, rule, row_index):
        payload_item_index = 0
        for column_index in rule.enumerate_column_indices():
            self._set_item_in_table(
                row_index, column_index, rule.payload_type, 
                payload_items[payload_item_index])
            payload_item_index = (payload_item_index + 1) % len(payload_items)

    def _in_blocks(self, payload_items, rule, row_index):
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
        self._table.rows[row_index][column_index][payload_type] = payload_item


class AllocTable():

    def __init__(self, n_rows, n_cols):
        """
        This mimics the structure of HTML <tr> and <td>.

        The table is modelled as an ordered sequence of rows.
        Each row is an ordered sequence of cells.
        Each cell is a dictionary keyed on strings like 'Strain'.
        The values against each of these keys is the string to display to
        represent that thing in the cell..

        Example for table row 2, column 3: (zero based indices).

            table[2][3]['PA Primers'] = 'Efm_vanA_1.x_van05_van01'
        """
        self.rows = []
        for row_idx in range(n_rows):
            row = []
            self.rows.append(row)
            for col in range(n_cols):
                row.append({})
                


