from app.rules_engine.rule_script_parser import RuleScriptParser
from app.rules_engine.rule_script_parser import ParseError
from app.rules_engine.rule_obj_interpreter import RulesObjInterpreter

class RulesScriptProcessor:
    """
    Orchestrates first the parsing of a rules script by RuleScriptParser, then
    the interpretation of the rule objects produced by RulesObjInterpreter.
    If there is a syntax error it provides (ParseError, None). 
    Otherwise (None, AllocationResults).
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
            machine_readable_rules = parser.results
        except ParseError as e:
            return (e, None)

        interpreter = RulesObjInterpreter(machine_readable_rules)
        alloc_table = interpreter.interpret()
        return (None, alloc_table)
        
