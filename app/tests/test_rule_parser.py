import unittest
from pdb import set_trace as st

from app.rules_engine.rule_script_parser import RuleScriptParser
from app.rules_engine.rule_script_parser import ParseError

class RuleScriptParserTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_example_from_language_spec(self):

        script = RuleScriptParserTest.trim_left(
        """ V ver-1
            P Plate1
            A Titanium-Taq              1-12  A-H 0.02 M/uL
            A (Eco)-ATCC-BAA-2355       1,5,9 B   1.16 x

            # This is a comment
            P Plate42
            T Plate1 1 B                1-12  A-H   20 dilution
        """)
        reagents = ('Titanium-Taq', '(Eco)-ATCC-BAA-2355')
        units = ('M/uL', 'x', 'dilution')
        parser = RuleScriptParser(reagents, units, script)
        rules = parser.parse()

        results = parser.results
        self.assertEqual(len(results), 9999)

    @classmethod
    def trim_left(cls, multiline_string):
        """
        Take a big string likely produced from a triple quoted string
        constant, and return a modified version, from which the leading spaces
        at the start of each line has been removed.
        """
        lines = multiline_string.split('\n')
        lines = (l.strip() for l in lines)
        return '\n'.join(lines)

