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
        results = parser.results

        # Start with the second plate results

        plate, rules = results.popitem()

        self.assertEqual(plate, 'Plate42')
        self.assertEqual(len(rules), 1)

        # This checks all the fields of a transfer rule, including
        # two of the row/col spec formats.
        rule = rules[0]
        self.assertEqual(rule.source_plate, 'Plate1')
        self.assertEqual(rule.s_cells.rows, [1])
        self.assertEqual(rule.s_cells.cols, [2])
        self.assertEqual(rule.d_cells.rows, [1,2,3,4,5,6,7,8,9,10,11,12])
        self.assertEqual(rule.d_cells.cols, [1,2,3,4,5,6,7,8])
        self.assertEqual(rule.conc, 20)
        self.assertEqual(rule.dilution_factor, 'dilution')

        # Move on to the second plate

        plate, rules = results.popitem()

        self.assertEqual(plate, 'Plate1')
        self.assertEqual(len(rules), 3)

        # This checks all the fields of an alloc rule, including
        # the remainder of the row/col specs.
        rule = rules[1]
        self.assertEqual(rule.reagent_name, '(Eco)-ATCC-BAA-2355')
        self.assertEqual(rule.cells.rows, [1,5,9])
        self.assertEqual(rule.cells.cols, [2,])
        self.assertEqual(rule.conc, 1.16)
        self.assertEqual(rule.units, 'x')

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

