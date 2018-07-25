
import os

from app.mob2dsl.user_input import get_user_allocation, get_pa_cols, \
    get_id_cols, get_sample_layout
from app.mob2dsl.allocation import make_nested_pa_dsl, make_nested_id_dsl, \
    make_nested_transfer_dsl


PATH = os.path.dirname(os.path.abspath(__file__))

DSL_VERSION = 'V ver-1'
PLATE_ROWS = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')


def generate_dsl(excel_file, pa_mastermix, pa_primer_conc, pa_primer_unit,
                 id_mastermix, id_primer_conc, id_primer_unit, dilution):

    excel = os.path.join(PATH, 'data', excel_file)
    plates = get_user_allocation(excel)
    pa_layout = get_sample_layout(excel, 'pa layout')
    id_layout = get_sample_layout(excel, 'id layout')

    dsl = [DSL_VERSION, '\n']
    for plate_id, plate in plates.items():
        pa_cols = get_pa_cols(plate)

        pa_dsl = make_nested_pa_dsl(plate, PLATE_ROWS, pa_cols,
                                    pa_mastermix, pa_primer_conc,
                                    pa_primer_unit, pa_layout)
        dsl = dsl + [f'P {plate_id}_PA'] + pa_dsl + ['\n']

        transfer = make_nested_transfer_dsl(f'{plate_id}_PA', PLATE_ROWS,
                                            pa_cols, dilution)

        id_cols = get_id_cols(plate)
        id_dsl = make_nested_id_dsl(plate, PLATE_ROWS, id_cols,
                                    id_mastermix, id_primer_conc,
                                    id_primer_unit, id_layout)

        dsl = dsl + [f'P {plate_id}_ID'] + id_dsl + transfer + ['\n']

    return dsl


if __name__ == '__main__':

    excel_file = 'nested_input_A.xlsx'

    pa_mastermix = 'pa mastermix A'
    id_mastermix = 'id mastermix A'

    pa_primer_conc = 0.4
    pa_primers_unit = 'uM'
    id_primer_conc = 0.9
    id_primers_unit = 'uM'
    dilution = 30

    dsl = generate_dsl(excel_file, pa_mastermix, pa_primer_conc,
                       pa_primers_unit, id_mastermix, id_primer_conc,
                       id_primers_unit, dilution)
    print('\n'.join(dsl))
