
import os
import pandas as pd
from app.mob2dsl.user_input import get_user_allocation, get_pa_cols, \
    get_id_cols, get_sample_layout
from app.mob2dsl.allocation import make_nested_pa_dsl, make_nested_id_dsl, \
    make_nested_transfer_dsl
from rest_framework.exceptions import ValidationError

PATH = os.path.dirname(os.path.abspath(__file__))

DSL_VERSION = 'V ver-1'
PLATE_ROWS = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')


def generate_dsl(file,options):

    ## check if all necessary options are available
    assert_options(options)
    ## Assignment from request options
    pa_mastermix  = options['pa_mastermix']
    pa_primer_conc= options['pa_primer_conc']
    pa_primer_unit= options['pa_primer_unit']
    id_mastermix = options['id_mastermix']
    id_primer_conc= options['id_primer_conc']
    id_primer_unit= options['id_primer_unit']
    dilution= options['dilution']

    excel_file = pd.ExcelFile(file)
    plates = get_user_allocation(excel_file)
    pa_layout = get_sample_layout(excel_file, 'pa layout')
    id_layout = get_sample_layout(excel_file, 'id layout')

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

def assert_options(options):
    necessary_options = ['pa_mastermix', 'pa_primer_conc', 'pa_primer_unit',
    'id_mastermix', 'id_primer_conc', 'id_primer_unit', 'dilution']

    if any(nec_op not in options for nec_op in necessary_options):
        raise ValidationError('Please provide {}'.format(','.join([nec_op for
                                                                   nec_op in
                                                         necessary_options if
                                                                   nec_op not in
                                                          options])))

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
