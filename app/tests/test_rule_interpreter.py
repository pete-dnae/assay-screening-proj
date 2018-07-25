import unittest
import re
from pdb import set_trace as st

from app.rules_engine.rule_script_parser import RuleScriptParser
from app.rules_engine.rule_script_parser import ParseError
from app.rules_engine.rule_obj_interpreter import RulesObjInterpreter
from app.model_builders.reference_data import REFERENCE_ALLOWED_NAMES
from app.model_builders.reference_data import REFERENCE_SCRIPT
from app.model_builders.reference_data import REFERENCE_UNITS


class RuleInterpreterTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_smallest_alloc_example_to_make_sure_row_col_right_way_round(self):
        # Cut the reference script to just a single allocation rule that
        # targets column 2, and row C (i.e. 3)
        regex = re.compile(r'Taq.*', re.DOTALL)
        script = re.sub(regex, 'Taq 2  C 0.02 M/uL', REFERENCE_SCRIPT)
        parser = RuleScriptParser(  
            REFERENCE_ALLOWED_NAMES, REFERENCE_UNITS, script)
        parser.parse()
        machine_readable_rules = parser.rule_objects
        interpreter = RulesObjInterpreter(machine_readable_rules)
        alloc_table,thermal_cycling_results = interpreter.interpret()
        # This should be the only cell included in the results.
        # And comprise one reagent.
        contents = alloc_table.plate_info['Plate1'][2][3]
        self.assertEqual(len(contents), 1)
        reagent, conc, units = contents[0]
        self.assertEqual(reagent, 'Titanium-Taq')

    def test_example_from_language_spec(self):
        parser = RuleScriptParser(  
            REFERENCE_ALLOWED_NAMES, REFERENCE_UNITS, REFERENCE_SCRIPT)
        parser.parse()
        machine_readable_rules = parser.rule_objects

        interpreter = RulesObjInterpreter(machine_readable_rules)
        # If any exceptions are raised in the call below, then in this case,
        # the test should fail.
        alloc_table,thermal_cycling_results = interpreter.interpret()

        # Sample the output where created with AllocRule(s)
        # Choose column 1, row B which is targeted by the first two rules.
        contents = alloc_table.plate_info['Plate1'][1][2]

        reagent, conc, units = contents[0]
        self.assertEqual(reagent, 'Titanium-Taq')
        self.assertEqual(conc, 0.02)
        self.assertEqual(units, 'M/uL')

        reagent, conc, units = contents[1]
        self.assertEqual(reagent, '(Eco)-ATCC-BAA-2355')
        self.assertEqual(conc, 1.16)
        self.assertEqual(units, 'x')

        # Sample the output where created with TransferRule(s)
        contents = alloc_table.plate_info['Plate42'][2][3]

        reagent, conc, units = contents[0]
        self.assertEqual(reagent, 'Transfer Plate1: Well B1')
        self.assertEqual(conc, 20.0)
        self.assertEqual(units, 'dilution')

        # Sample the output where created using a reagent group name.
        contents = alloc_table.plate_info['Plate42'][1][1]

        reagent, conc, units = contents[1]
        self.assertEqual(reagent, 'Pool_1')
        self.assertEqual(conc, 1.0)
        self.assertEqual(units, 'x')

        contents = thermal_cycling_results.plate_info['Plate1'][0]
        self.assertEqual(contents['temperature_steps'], '10Sec at 95°C, 12Sec at 60°C, 15Sec at 65°C, ')
        contents = thermal_cycling_results.plate_info['Plate1'][1]
        self.assertEqual(contents['temperature_steps'], '7Sec at 60°C, 10Sec at 65°C, 10Sec at 95°C, ')