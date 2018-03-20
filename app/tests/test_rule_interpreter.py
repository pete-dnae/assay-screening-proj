import unittest
from pdb import set_trace as st

from app.rules_engine.rule_script_parser import RuleScriptParser
from app.rules_engine.rule_script_parser import ParseError
from app.rules_engine.rule_obj_interpreter import RulesObjInterpreter
from app.model_builders.reference_rules_script import REFERENCE_SCRIPT

class RuleInterpreterTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_example_from_language_spec(self):
        reagents = (
            'Titanium-Taq',
            '(Eco)-ATCC-BAA-2355',
            '(Eco)-ATCC-BAA-9999')
        units = ('M/uL', 'x', 'dilution')
        parser = RuleScriptParser(reagents, units, REFERENCE_SCRIPT)
        parser.parse()
        machine_readable_rules = parser.results

        interpreter = RulesObjInterpreter(machine_readable_rules)
        # If any exceptions are raised in the call below, then in this case,
        # the test should fail.
        alloc_table = interpreter.interpret()

        # Sample the output where created with AllocRule(s)
        contents = alloc_table.data['Plate1'][1][2]

        reagent, conc, units = contents[0]
        self.assertEqual(reagent, 'Titanium-Taq')
        self.assertEqual(conc, 0.02)
        self.assertEqual(units, 'M/uL')

        reagent, conc, units = contents[1]
        self.assertEqual(reagent, '(Eco)-ATCC-BAA-2355')
        self.assertEqual(conc, 1.16)
        self.assertEqual(units, 'x')

        # Sample the output where created with TransferRule(s)
        contents = alloc_table.data['Plate42'][2][3]

        reagent, conc, units = contents[0]
        self.assertEqual(reagent, 'Transfer Plate42:Row-1:Col-2')
        self.assertEqual(conc, 20.0)
        self.assertEqual(units, 'dilution')
