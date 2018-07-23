
import os

from app.mob2dsl.user_input import get_user_allocation, get_allocated_cols, \
    get_user_sample_layout
from app.mob2dsl.allocation import make_nested_pa_dsl, make_nested_id_dsl, \
    make_nested_transfer_dsl


PATH = os.path.dirname(os.path.abspath(__file__))

DSL_VERSION = 'V ver-1'
PLATE_ROWS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']


if __name__ == '__main__':

    EXP_TYPE = 'NESTED'

    SAMPLE_LAYOUT = "layout A"
    PA_MASTERMIX = 'pa mastermix A'
    ID_MASTERMIX = 'id mastermix A'

    PA_PRIMERS_CONC = 0.4
    PA_PRIMERS_UNIT = 'uM'
    ID_PRIMERS_CONC = 0.9
    ID_PRIMERS_UNIT = 'uM'
    DILUTION = 30

    excel = os.path.join(PATH, 'user_input.xlsx')
    plates = get_user_allocation(excel)
    sample_layout = get_user_sample_layout(excel)

    dsl = [DSL_VERSION, '\n']
    for plate_id, plate in plates.items():
        allocated_cols = get_allocated_cols(plate)

        pa_dsl = make_nested_pa_dsl(plate, PLATE_ROWS, allocated_cols,
                                    PA_MASTERMIX, PA_PRIMERS_CONC,
                                    PA_PRIMERS_UNIT, sample_layout)
        dsl = dsl + ['P {}_PA'.format(plate_id)] + pa_dsl + ['\n']

        transfer = make_nested_transfer_dsl(plate_id + '_PA', PLATE_ROWS,
                                            allocated_cols, DILUTION)
        id_dsl = make_nested_id_dsl(plate, PLATE_ROWS, allocated_cols,
                                    ID_MASTERMIX, ID_PRIMERS_CONC,
                                    ID_PRIMERS_UNIT)

        dsl = dsl + ['P {}_ID'.format(plate_id)] + id_dsl + transfer + ['\n']

    print('\n'.join(dsl))
