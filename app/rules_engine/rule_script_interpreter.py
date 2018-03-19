from app.rules_engine.rule_script_parser import RuleScriptParser
from app.rules_engine.rule_script_parser import ParseError
from app.rules_engine.rule_interpreter import RuleInterpreter

class RulesScriptInterpreter:
    """
    Parses, AND interprets a rules script. If there is a syntax error it
    provides (ParseError, None). Otherwise (None, AllocTable).
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

        interpreter = RuleInterpreter(machine_readable_rules)
        alloc_table = interpreter.interpret()
        return (None, alloc_table)
        
