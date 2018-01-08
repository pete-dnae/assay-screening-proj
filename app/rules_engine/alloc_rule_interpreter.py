from collections import defaultdict


class AllocRuleInterpreter:

    def __init__(self, rules):
        self._rules = rules
        self._n_rows = None
        self._n_cols = None

    def interpret(self):
        self._n_rows = \
            1 + ord(max((r.end_row_letter for r in self._rules))) - ord('A')
        self._n_cols = max((r.end_column for r in self._rules))

        table = {} # keyed on row then column.
        for rule in self._rules:
            self._apply_rule_to_table(rule, table)
        return(table)

    def _apply_rule_to_table(self, rule, table):
        row_letter = rule.start_row_letter
        while True:
            row_dict = {}
            table[row_letter] = row_dict
            self._apply_to_row(rule, row_dict)
            if row_letter == rule.end_row_letter:
                break
            row_letter = chr(ord(row_letter) + 1)
        pass

    def _apply_to_row(self, rule, row_dict):
        columns = [i for i in range(rule.start_column, rule.end_column + 1)]
        if rule.pattern is 'Consecutive':
            self._consecutive(row_dict, columns, rule)
        elif rule.pattern is 'In Blocks':
            self._inblocks(row_dict, columns, rule)

    def _consecutive(self, row_dict, columns, rule):
        pass

    def _in_blocks(self, row_dict, columns, rule):
        pass
