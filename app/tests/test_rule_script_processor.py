import unittest
from pdb import set_trace as st

from app.rules_engine.rule_script_processor import RulesScriptProcessor
from app.rules_engine.rule_script_parser import ParseError
from app.model_builders.reference_data import REFERENCE_SCRIPT

class RuleScriptProcessorTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_on_properly_formed_rules_script(self):
        reagents = (
            'Titanium-Taq',
            '(Eco)-ATCC-BAA-2355',
            '(Eco)-ATCC-BAA-9999')
        units = ('M/uL', 'x', 'dilution')
        interpreter = RulesScriptProcessor(REFERENCE_SCRIPT, reagents, units)
        parse_error, alloc_table, line_number_to_cells_mapping = \
                interpreter.parse_and_interpret()

        # Make sure no error is reported.
        self.assertIsNone(parse_error)

        # Make sure AllocationResults is returned and seems well-formed.
        self.assertIsNotNone(alloc_table)
        self.assertTrue('Plate1' in alloc_table.plate_info)

        # Make sure the line number to cells mapping looks ok.
        self.assertEqual(
            line_number_to_cells_mapping[4],
            [(1, 2), (5, 2), (9, 2)])

    def test_on_malformed_rules_script(self):
        reagents = (
            'Titanium-Taq',
            '(Eco)-ATCC-BAA-2355',
            '(Eco)-ATCC-BAA-9999')
        units = ('M/uL', 'x', 'dilution')
        broken_script = REFERENCE_SCRIPT.replace('A (Eco', 'Q (Eco')
        interpreter = RulesScriptProcessor(broken_script, reagents, units)
        parse_error, alloc_table, line_number_to_cells_mapping = \
                interpreter.parse_and_interpret()
        self.assertEqual(parse_error.message,
                'Line must start with one of the letters V|P|A|T. Line 4.')
