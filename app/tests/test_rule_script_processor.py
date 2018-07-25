import unittest
from pdb import set_trace as st

from app.rules_engine.rule_script_processor import RulesScriptProcessor
from app.rules_engine.rule_script_parser import ParseError
from app.model_builders.reference_data import REFERENCE_SCRIPT
from app.model_builders.reference_data import REFERENCE_ALLOWED_NAMES
from app.model_builders.reference_data import REFERENCE_UNITS

class RuleScriptProcessorTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_on_properly_formed_rules_script(self):
        interpreter = RulesScriptProcessor(
            REFERENCE_SCRIPT, REFERENCE_ALLOWED_NAMES, REFERENCE_UNITS)
        parse_error, alloc_table,thermal_cycling_results, line_number_to_cells_mapping = \
                interpreter.parse_and_interpret()

        # Make sure no error is reported.
        self.assertIsNone(parse_error)

        # Make sure AllocationResults is returned and seems well-formed.
        self.assertIsNotNone(alloc_table)
        self.assertTrue('Plate1' in alloc_table.plate_info)
        self.assertTrue('Plate42' in alloc_table.plate_info)

        # Check sampled contents, including a reagent group.
        cell_contents = alloc_table.plate_info['Plate42'][1][1]
        self.assertEqual(cell_contents[0], 
            ('Transfer Plate1: Well B1', 20.0, 'dilution'))
        self.assertEqual(cell_contents[1], 
            ('Pool_1', 1.0, 'x'))

        # Make sure the line number to cells mapping looks ok.
        self.assertEqual(
            line_number_to_cells_mapping[4], [(1, 2), (5, 2), (9, 2)])

        cell_contents = thermal_cycling_results.plate_info['Plate1'][0]
        expected_element ={
            'temperature_steps':'10Sec at 95°C, 12Sec at 60°C, 15Sec at 65°C, ',
            'cycles': '5',
            'units': 'x'
        }
        self.assertEquals(cell_contents,expected_element)



    def test_on_malformed_rules_script(self):
        broken_script = REFERENCE_SCRIPT.replace('A (Eco', 'Q (Eco')
        interpreter = RulesScriptProcessor(
            broken_script, REFERENCE_ALLOWED_NAMES, REFERENCE_UNITS)
        parse_error, alloc_table,thermal_cycling_results, line_number_to_cells_mapping = \
                interpreter.parse_and_interpret()
        self.assertEqual(parse_error.message,
                'Line must start with one of the letters V|P|A|T|C. Line 4.')
