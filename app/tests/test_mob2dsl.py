import unittest
from app.mob2dsl.nested import generate_dsl

class Mob2Dsl(unittest.TestCase):

    def setUp(self):
        pass

    def test_mob2dsl(self):
        pa_mastermix = 'pa mastermix A'
        id_mastermix = 'id mastermix A'

        pa_primer_conc = 0.4
        pa_primers_unit = 'uM'
        id_primer_conc = 0.9
        id_primers_unit = 'uM'
        dilution = 30
        excel_file = 'nested_input_A.xlsx'

        dsl = generate_dsl(excel_file, pa_mastermix, pa_primer_conc,
                           pa_primers_unit, id_mastermix, id_primer_conc,
                           id_primers_unit, dilution)
        print('\n'.join(dsl))