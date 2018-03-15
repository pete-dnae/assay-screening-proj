from collections import defaultdict

class AllocationResults():
    """
    This is used by AllocRuleInterpreter to deliver its results.

    A table-like data structure representing a grid of chambers on a 
    plate and for each cell, a list of what has been allocated to it.
    We use 1-based indices to make it easier to carry through users' ideas
    about how rows and columns are numbered.
    """

    def __init__(self):
        """
        The table is indexed on row then column like this.

            table[1][3] = [name1,name2,name3...]
        """
        self.rows = defaultdict(dict)

    def add(self, row, col, reagent_name):
        self.rows[row].setdefault(col, []).append(reagent)


class AllocRuleInterpreter:
    """
    This class owns the business logic that knows how to interpret a sequence
    of heterogeneous AllocRule(s) and TransferRule(s).

    It returns an AllocTable.
    """

    def __init__(self, rules):
        """
        Provide a sequence comprising any mix of AllocRule | TransferRule.
        """
        self._rules = rules
        self._table = None

    def interpret(self):
        for rule in self._rules:
            if isinstance(rule, AllocRule):
                self._apply_alloc_rule(rule)
            elif isinstance(rule, TransferRule):
                self._apply_transfer_rule(rule)
            else:
                raise TypeError('Rule type not recognized')
        return(self._table)

    def _apply_alloc_rule(self, rule):
        pass

    def _apply_transfer_rule(self, rule):
        pass


