from collections import OrderedDict
from pdb import set_trace as st

from app.rules_engine.alloc_rule import AllocRule
from app.rules_engine.transfer_rule import TransferRule

class AllocationResults():
    """
    This is used by AllocRuleInterpreter to deliver its results.
    It's a data structure along these lines:

        data[plate_name][row][col] = (item1, item2, ... item_n)

    Where an item looks like:

        (reagent_name, concentration_value, concentration_units)

    We use 1-based indices to make it easier to carry through users' ideas
    about how rows and columns are numbered.

    The dictionaries are OrderedDict(s)
    """

    def __init__(self):
        self.data = OrderedDict()

    def add(self, plate, row, col, reagent_name, conc, units):
        rows = self.data.setdefault(plate, OrderedDict())
        cols = rows.setdefault(row, OrderedDict())
        reagents = cols.setdefault(col, [])
        reagents.append((reagent_name, conc, units))


class RuleInterpreter:
    """
    This class owns the business logic that knows how to interpret a sequence
    of heterogeneous AllocRule(s) and TransferRule(s).

    It returns an AllocTable.
    """

    def __init__(self, plates_with_rules):
        """
        Provide a dictionary keyed on plate names, with values that are a
        sequence comprising any mix of AllocRule | TransferRule.
        """
        self._plates_with_rules = plates_with_rules
        self._allocation_results = AllocationResults()

    def interpret(self):
        for plate, rules in self._plates_with_rules.items():
            for rule in rules:
                if isinstance(rule, AllocRule):
                    self._apply_alloc_rule(plate, rule)
                elif isinstance(rule, TransferRule):
                    self._apply_transfer_rule(plate, rule)
                else:
                    raise TypeError('Rule type not recognized')
        return(self._allocation_results)

    def _apply_alloc_rule(self, plate, rule):
        for row, col in rule.cells.all_cells():
            self._allocation_results.add(plate, row, col, rule.reagent_name,
                    rule.conc, rule.units)

    def _apply_transfer_rule(self, plate, rule):
        pass


