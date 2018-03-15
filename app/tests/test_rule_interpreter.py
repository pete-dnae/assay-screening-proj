import unittest
from pdb import set_trace as st

from app.rules_engine.rule_script_parser import RuleScriptParser
from app.rules_engine.rule_script_parser import ParseError
from app.rules_engine.rule_interpreter import RuleInterpreter

class RuleInterpreterTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_example_from_language_spec(self):
        # Easiest, (if not most de-coupled) way to start.

        script = _trim_left(
        """ V ver-1
            P Plate1
            A Titanium-Taq              1-12  A-H 0.02 M/uL
            A (Eco)-ATCC-BAA-2355       1,5,9 B   1.16 x
            A (Eco)-ATCC-BAA-9999       2     C,D 1.16 x

            # This is a comment
            P Plate42
            T Plate1 1 B                1-12  A-H   20 dilution
        """)
        reagents = (
            'Titanium-Taq',
            '(Eco)-ATCC-BAA-2355',
            '(Eco)-ATCC-BAA-9999')
        units = ('M/uL', 'x', 'dilution')
        parser = RuleScriptParser(reagents, units, script)
        parser.parse()
        machine_readable_rules = parser.results

        interpreter = RuleInterpreter(machine_readable_rules)
        # If any exceptions are raised in the call below, then in this case,
        # the test should fail.
        alloc_table = interpreter.interpret()

        # Smoke test for contents
        contents = alloc_table.data['Plate1'][1][2]

        reagent, conc, units = contents[0]
        self.assertEqual(reagent, 'Titanium-Taq')
        self.assertEqual(conc, 0.02)
        self.assertEqual(units, 'M/uL')

        reagent, conc, units = contents[1]
        self.assertEqual(reagent, '(Eco)-ATCC-BAA-2355')
        self.assertEqual(conc, 1.16)
        self.assertEqual(units, 'x')

def _trim_left(multiline_string):
    """
    Take a big string likely produced from a triple quoted string
    constant, and return a modified version, from which the leading spaces
    at the start of each line has been removed.
    """
    lines = multiline_string.split('\n')
    lines = (l.strip() for l in lines)
    return '\n'.join(lines)

