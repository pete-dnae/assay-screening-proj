from collections import OrderedDict
from pdb import set_trace as st

from app.rules_engine.alloc_rule import AllocRule
from app.rules_engine.transfer_rule import TransferRule
from app.rules_engine.thermal_cycle_rule import ThermalCycleRule


class RulesObjInterpreter:
    """
    This class owns the business logic that knows how to interpret a sequence
    of heterogeneous AllocRule(s) , TransferRule(s) and ThermalCyclingRule(s).

    It returns  AllocResults and ThermalCyclingResults . (defined later in this module)
    """

    def __init__(self, plates_with_rules):
        """
        Provide a dictionary keyed on plate names, with values that are a
        sequence comprising any mix of AllocRule | TransferRule.
        """
        self._plates_with_rules = plates_with_rules
        self._allocation_results = None # AllocationResults
        self._thermal_cycling_results = None

    def interpret(self):
        """
        Returns  AllocationResults object and ThermalCyclingResults Object.
        """

        self._allocation_results = AllocationResults()
        self._thermal_cycling_results = ThermalCyclingResults()
        for plate, rules in self._plates_with_rules.items():
            for rule in rules:
                if isinstance(rule, AllocRule):
                    self._apply_alloc_rule(plate, rule)
                elif isinstance(rule, TransferRule):
                    self._apply_transfer_rule(plate, rule)
                elif isinstance(rule, ThermalCycleRule):
                    self._apply_thermal_cycle_rule(plate, rule)
                else:
                    raise TypeError('Rule type not recognized')
        return self._allocation_results,self._thermal_cycling_results

    def _apply_alloc_rule(self, plate, rule):
        for row, col in rule.cells.all_cells():
            self._allocation_results.add(plate, row, col, rule.reagent_name,
                    rule.conc, rule.units)
            self._allocation_results.void_source(plate, row, col)

    def _apply_transfer_rule(self, plate, rule):
        for d_row, d_col in rule.d_cells.all_cells():
            s_col, s_row = rule.mapping[d_col][d_row]
            s_plate = rule.source_plate
            virtual_reagent_name = \
                'Transfer %s:Col-%d:Row-%d' % (s_plate, s_col, s_row)
            self._allocation_results.add(plate, d_row, d_col, 
                    virtual_reagent_name, rule.dilution_factor, 'dilution')
            self._allocation_results.add_source(plate,d_row,d_col,s_row,
                                                s_col,s_plate)

    def _apply_thermal_cycle_rule(self, plate, rule):
        self._thermal_cycling_results.add(plate,rule.todict())


class AllocationResults:

    """
    This is used by RulesObjInterpreter to deliver its results.
    It's a data structure along these lines:

       .plate_info[plate_name][col][row] = (item1, item2, ... item_n)

    Where an item looks like:

        (reagent_name, concentration_value, concentration_units)

    Also It carries information about source plate whenever need be

        .source_col_map[plate_name][col][row]={'source_row':foo,
                                                'source_col':fee,
                                                'source_plate':faa}

    We use 1-based indices to make it easier to carry through users' ideas
    about how rows and columns are numbered.

    The dictionaries are OrderedDict(s)
    """

    def __init__(self):
        self.plate_info = OrderedDict()
        self.source_map = OrderedDict()

    def add(self, plate, row, col, reagent_name, conc, units):
        cols = self.plate_info.setdefault(plate, OrderedDict())
        rows = cols.setdefault(col, OrderedDict())
        reagents = rows.setdefault(row, [])
        reagents.append((reagent_name, conc, units))

    def add_source(self,plate,row,col,source_row,source_col,source_plate):
        cols = self.source_map.setdefault(plate, OrderedDict())
        rows = cols.setdefault(col, OrderedDict())
        source_info = rows.setdefault(row, {})
        source_info.update({'source_row':source_row,'source_col':source_col,
                     'source_plate':source_plate})

    def void_source(self,plate,row,col):
        cols = self.source_map.setdefault(plate, OrderedDict())
        rows = cols.setdefault(col, OrderedDict())
        rows.setdefault(row, {})

class ThermalCyclingResults:

    """
    Used by RulesObjInterpreter to deliver interpretation of thermal cycling
    rules

    Data structure skeleton below :
        .plate_info[plate_name]=[item1,item2]

    Where an Item looks like
        item1={
            temperature_steps:'12 seconds at 95 C ,15 seconds at 60C',
            repeat_cycles: 5,
            units:x
        }
        The dictionaries are OrderedDict(s)
    """

    def __init__(self):
        self.plate_info = OrderedDict()

    def add(self, plate,thermal_cycling_item):
        self.plate_info.setdefault(plate, []).append(thermal_cycling_item)

