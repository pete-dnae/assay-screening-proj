import unittest
from pdb import set_trace as st

from app.rules_engine.rule_script_parser import RuleScriptParser
from app.rules_engine.rule_script_parser import ParseError
from app.model_builders.reference_rules_script import REFERENCE_SCRIPT

class RuleScriptParserTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_example_from_language_spec(self):
        parser = RuleScriptParser(STD_REAGENTS, STD_UNITS, REFERENCE_SCRIPT)
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
        self.assertEqual(rule.dilution_factor, 20)

        # Move back to the first plate

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

    def test_error_wrong_letter_at_start_of_line(self):
        modified_script = REFERENCE_SCRIPT.replace('A Titani', 'N Titani')
        parser = RuleScriptParser(STD_REAGENTS, STD_UNITS, modified_script)
        with self.assertRaises(ParseError) as cm:
            parser.parse()
        e = cm.exception
        self.assertEqual(e.message,
            'Line must start with one of the letters V|P|A|T. Line 3.')
        self.assertEqual(e.where_in_script, 17)

    def test_error_wrong_version(self):
        modified_script = REFERENCE_SCRIPT.replace('ver-1', 'fibble')
        parser = RuleScriptParser(STD_REAGENTS, STD_UNITS, modified_script)
        with self.assertRaises(ParseError) as cm:
            parser.parse()
        e = cm.exception
        self.assertEqual(e.message,
            'Your script version is not recognized by this parser. ' + \
            'Line 1. Character 3.')
        self.assertEqual(e.where_in_script, 2)


STD_REAGENTS = (
            'Titanium-Taq',
            '(Eco)-ATCC-BAA-2355',
            '(Eco)-ATCC-BAA-9999')

STD_UNITS = ('M/uL', 'x', 'dilution')
