
import os
import unittest
import pandas as pd

from app.mob2dsl.nested_main import PATH, generate_dsl
from app.mob2dsl.dsl import standardize_conc


class TestNestedA(unittest.TestCase):

    def setUp(self):
        self.excel_file = os.path.join(PATH, 'data', 'nested_input_A.xlsx')
        self.rules_script = _make_rules_script(self.excel_file)

    def test_nested_a(self):

        pa_mastermix = 'pa mastermix A'
        id_mastermix = 'id mastermix A'

        pa_primer_conc = 0.4
        pa_primers_unit = 'uM'
        id_primer_conc = 0.9
        id_primers_unit = 'uM'
        dilution = 30

        dsl = generate_dsl(self.excel_file, pa_mastermix, pa_primer_conc,
                           pa_primers_unit, id_mastermix, id_primer_conc,
                           id_primers_unit, dilution)
        dsl = [l for l in dsl if l != 'V ver-1']
        dsl = [l for l in dsl if l != '\n']
        self.assertEqual(set(self.rules_script), set(dsl))


class TestNestedB(unittest.TestCase):

    def setUp(self):
        self.excel_file = os.path.join(PATH, 'data', 'nested_input_B.xlsx')
        self.rules_script = _make_rules_script(self.excel_file)

    def test_nested_b(self):
        pa_mastermix = 'pa mastermix A'
        id_mastermix = 'id mastermix A'

        pa_primer_conc = 0.4
        pa_primers_unit = 'uM'
        id_primer_conc = 0.4
        id_primers_unit = 'uM'
        dilution = 30

        dsl = generate_dsl(self.excel_file, pa_mastermix, pa_primer_conc,
                           pa_primers_unit, id_mastermix, id_primer_conc,
                           id_primers_unit, dilution)
        dsl = [l for l in dsl if l != 'V ver-1']
        dsl = [l for l in dsl if l != '\n']
        self.assertEqual(set(self.rules_script), set(dsl))


def _make_rules_script(excel):

    df = pd.read_excel(excel, sheet_name='rules script', header=None)
    rules_script = []
    for _, row in df.iterrows():
        rule, reagent, cols, rows, conc, unit, dil_factor, dilution = \
            row.fillna('').values
        if rule == 'A':
            line = f'{rule} {reagent} {cols} {rows} ' \
                   f'{standardize_conc(conc)} {unit}'
            rules_script.append(line)
        elif rule == 'T':
            line = f'{rule} {reagent} {cols} {rows} ' \
                   f'{conc} {unit} {int(dil_factor)} {dilution}'
            rules_script.append(line)
        elif rule == 'P':
            line = f'{rule} {reagent}'
            rules_script.append(line)
        else:
            pass

    return rules_script