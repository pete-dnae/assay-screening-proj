import unittest
from pdb import set_trace as st

from app.rules_engine.rule_script_parser import RuleScriptParser
from app.rules_engine.rule_script_parser import ParseError
from app.model_builders.reference_data import REFERENCE_SCRIPT
from app.model_builders.reference_data import REFERENCE_REAGENT_NAMES
from app.model_builders.reference_data import REFERENCE_UNITS

class RuleScriptParserTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_example_from_language_spec(self):
        """
        Provide the parser with a valid input script, and make sure the machine
        readable results are properly formed.
        """
        parser = RuleScriptParser(
                REFERENCE_REAGENT_NAMES, REFERENCE_UNITS, REFERENCE_SCRIPT)
        parser.parse()
        rule_objects = parser.rule_objects

        # Start with the second plate results

        plate, rules = rule_objects.popitem()

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

        plate, rules = rule_objects.popitem()

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

        # Check a sample of the mapping back from parse objects to script
        # line number provenance.
        rule = rules[0]
        lnum = parser.line_number_mapping[rule]
        self.assertEqual(lnum, 3)

    #----------------------------------------------------------------------
    # Test the correct error handling for every error the parser can produce.
    #----------------------------------------------------------------------

    def test_error_wrong_letter_at_start_of_line(self):
        modified_script = REFERENCE_SCRIPT.replace('A Titani', 'N Titani')
        parser = RuleScriptParser(
                REFERENCE_REAGENT_NAMES, REFERENCE_UNITS, modified_script)
        with self.assertRaises(ParseError) as cm:
            parser.parse()
        e = cm.exception
        self.assertEqual(e.message,
            'Line must start with one of the letters V|P|A|T. Line 3.')
        self.assertEqual(e.where_in_script, 17)

    def test_error_wrong_version(self):
        modified_script = REFERENCE_SCRIPT.replace('ver-1', 'fibble')
        parser = RuleScriptParser(
                REFERENCE_REAGENT_NAMES, REFERENCE_UNITS, modified_script)
        with self.assertRaises(ParseError) as cm:
            parser.parse()
        e = cm.exception
        self.assertEqual(e.message,
            'Your script version is not recognized by this parser. ' + \
            'Line 1. Character 3.')
        self.assertEqual(e.where_in_script, 2)

    def test_error_transfer_incompatible(self):
        modified_script = REFERENCE_SCRIPT.replace('T Plate1 1', 'T Plate 1,2')
        parser = RuleScriptParser(
                REFERENCE_REAGENT_NAMES, REFERENCE_UNITS, modified_script)
        with self.assertRaises(ParseError) as cm:
            parser.parse()
        e = cm.exception
        self.assertEqual(e.message,
            'Shape of source rows/columns is incompatible with that of ' + \
            'destination. Line 8.')
        self.assertEqual(e.where_in_script, 185)

    def test_error_no_plate_defined_yet(self):
        modified_script = REFERENCE_SCRIPT.replace('P Plate1', '')
        parser = RuleScriptParser(
                REFERENCE_REAGENT_NAMES, REFERENCE_UNITS, modified_script)
        with self.assertRaises(ParseError) as cm:
            parser.parse()
        e = cm.exception
        self.assertEqual(e.message,
            'You must define a plate before this. Line 3.')
        self.assertEqual(e.where_in_script, 9)

    def test_error_plate_reused(self):
        modified_script = REFERENCE_SCRIPT.replace('P Plate42', 'P Plate1')
        parser = RuleScriptParser(
                REFERENCE_REAGENT_NAMES, REFERENCE_UNITS, modified_script)
        with self.assertRaises(ParseError) as cm:
            parser.parse()
        e = cm.exception
        self.assertEqual(e.message,
            'This plate name been used before. Line 7. Character 3.')
        self.assertEqual(e.where_in_script, 177)

    def test_error_unknown_reagent(self):
        modified_script = REFERENCE_SCRIPT.replace(
                'Titanium-Taq', 'Qitanium-Taq')
        parser = RuleScriptParser(
                REFERENCE_REAGENT_NAMES, REFERENCE_UNITS, modified_script)
        with self.assertRaises(ParseError) as cm:
            parser.parse()
        e = cm.exception
        self.assertEqual(e.message,
            'Unknown reagent. Line 3. Character 3.')
        self.assertEqual(e.where_in_script, 19)

    def test_error_unknown_units(self):
        modified_script = REFERENCE_SCRIPT.replace('M/uL', 'A/uL')
        parser = RuleScriptParser(
                REFERENCE_REAGENT_NAMES, REFERENCE_UNITS, modified_script)
        with self.assertRaises(ParseError) as cm:
            parser.parse()
        e = cm.exception
        self.assertEqual(e.message,
            'Unknown units. Line 3. Character 44.')
        self.assertEqual(e.where_in_script, 60)

    def test_error_transfer_must_use_dilution_as_units(self):
        modified_script = REFERENCE_SCRIPT.replace('dilution', 'ailution')
        parser = RuleScriptParser(
                REFERENCE_REAGENT_NAMES, REFERENCE_UNITS, modified_script)
        with self.assertRaises(ParseError) as cm:
            parser.parse()
        e = cm.exception
        self.assertEqual(e.message,
            'Units for a transfer must be <dilution>. Line 8. Character 44.')
        self.assertEqual(e.where_in_script, 228)

    def test_error_non_number_in_row(self):
        modified_script = REFERENCE_SCRIPT.replace('1,5,9', '1,A,9')
        parser = RuleScriptParser(
                REFERENCE_REAGENT_NAMES, REFERENCE_UNITS, modified_script)
        with self.assertRaises(ParseError) as cm:
            parser.parse()
        e = cm.exception
        self.assertEqual(e.message,
            'Struggling with a non-number in rows specification. ' + \
            'Line 4. Character 29.')
        self.assertEqual(e.where_in_script, 93)

    def test_error_concentration_not_numeric(self):
        modified_script = REFERENCE_SCRIPT.replace('0.02', 'fibble')
        parser = RuleScriptParser(
                REFERENCE_REAGENT_NAMES, REFERENCE_UNITS, modified_script)
        with self.assertRaises(ParseError) as cm:
            parser.parse()
        e = cm.exception
        self.assertEqual(e.message,
            'Cannot convert concentration to a number. Line 3. Character 39.')
        self.assertEqual(e.where_in_script, 55)

    def test_error_non_letter_in_column_spec(self):
        modified_script = REFERENCE_SCRIPT.replace('C,D', 'C,3')
        parser = RuleScriptParser(
                REFERENCE_REAGENT_NAMES, REFERENCE_UNITS, modified_script)
        with self.assertRaises(ParseError) as cm:
            parser.parse()
        e = cm.exception
        self.assertEqual(e.message,
            'Only letters allowed in columns specification. ' + \
            'Line 5. Character 35.')
        self.assertEqual(e.where_in_script, 144)

    def test_error_too_fiew_fields(self):
        modified_script = REFERENCE_SCRIPT.replace('M/uL', '')
        parser = RuleScriptParser(
                REFERENCE_REAGENT_NAMES, REFERENCE_UNITS, modified_script)
        with self.assertRaises(ParseError) as cm:
            parser.parse()
        e = cm.exception
        self.assertEqual(e.message,
            'Field number 6 (Concentration units) is missing. Line 3.')
        self.assertEqual(e.where_in_script, 17)

    def test_error_version_in_line_other_than_first(self):
        # Add a perfectly legal version line at the start, so that the
        # existing one will fall onto line 2 and thus illegal.
        modified_script = 'V ver-1\n' + REFERENCE_SCRIPT
        parser = RuleScriptParser(
                REFERENCE_REAGENT_NAMES, REFERENCE_UNITS, modified_script)
        with self.assertRaises(ParseError) as cm:
            parser.parse()
        e = cm.exception
        self.assertEqual(e.message,
            'Version must be specified in the first line. Line 2.')
        self.assertEqual(e.where_in_script, 8)

    def test_error_version_never_specified(self):
        modified_script = REFERENCE_SCRIPT.replace('V ver-1', '')
        parser = RuleScriptParser(
                REFERENCE_REAGENT_NAMES, REFERENCE_UNITS, modified_script)
        with self.assertRaises(ParseError) as cm:
            parser.parse()
        e = cm.exception
        self.assertEqual(e.message,
            'You must specify a version (in the first line). Line 8.')
        self.assertEqual(e.where_in_script, 178)
