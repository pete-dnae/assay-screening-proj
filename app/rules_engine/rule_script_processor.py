from collections import defaultdict
from pdb import set_trace as st

from app.rules_engine.rule_script_parser import RuleScriptParser
from app.rules_engine.rule_script_parser import ParseError
from app.rules_engine.alloc_rule import AllocRule
from app.rules_engine.transfer_rule import TransferRule
from app.rules_engine.rule_obj_interpreter import RulesObjInterpreter

class RulesScriptProcessor:
    """
    Orchestrates first the parsing of a rules script by RuleScriptParser, then
    the interpretation of the rule objects produced by RulesObjInterpreter.
    If there is a syntax error it provides (ParseError, None, None). 
    Otherwise (None, AllocationResults, line_number_to_cells_mapping).

    The line_number_to_cells_mapping works like this:
        line_number_to_cells_mapping[3] = ((1,2), (3,4), ...)
    """

    def __init__(self, rules_script, allowed_reagents, allowed_units):
        self._script = rules_script
        self._reagents = allowed_reagents
        self._units = allowed_units

    def parse_and_interpret(self):
        try:
            parser = RuleScriptParser(
                    self._reagents, self._units, self._script)
            parser.parse()
        except ParseError as e:
            return (e, None,None, None)

        interpreter = RulesObjInterpreter(parser.rule_objects)
        alloc_table,thermal_cycling_results = interpreter.interpret()
        line_number_to_cells_mapping = \
            self._make_line_number_to_cells_mapping(parser)
        return (None, alloc_table,thermal_cycling_results, dict(line_number_to_cells_mapping))
        
    def _make_line_number_to_cells_mapping(self, parser):
        """
        Returns a dictionary that maps script line numbers to the cells the
        rule on that line targets.
        """
        mapping = defaultdict(list)
        for plate, rule_objects in parser.rule_objects.items():
            for rule_obj in rule_objects:
                line_number = parser.line_number_mapping[rule_obj]
                if isinstance(rule_obj, AllocRule):
                    cells = rule_obj.cells
                elif isinstance(rule_obj, TransferRule):
                    cells = rule_obj.d_cells
                # These *cells* are ordered [(row,col), (row,col)...]
                # whereas we want [(col,row), (col,row)...] in ouput.
                transposed = [(col, row) for row, col in cells.all_cells()]
                mapping[line_number].extend(transposed)
        return mapping
