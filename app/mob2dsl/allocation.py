

from app.mob2dsl.mastermix import get_mastermix
from app.mob2dsl.sample_layout import get_sample_layout

PLATE_COLS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
PLATE_ROWS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

PLATE = 'A81_E361_1'
EXP_TYPE = 'NESTED'

SAMPLE_LAYOUT = "layout A"
PA_MASTERMIX = 'pa mastermix A'
ID_MASTERMIX = 'id mastermix A'

PA_PRIMERS_CONC = 0.4
PA_PRIMERS_UNIT = 'uM'
ID_PRIMERS_CONC = 0.9
ID_PRIMERS_UNIT = 'uM'

# Values are ordered by columns within each heading
ALLOCATION = {
    'ID Primers': [
        'AMR_NDM_x.3_NDM19_NDM21', 'AMR_NDM_x.3_NDM19_NDM21',
        'AMR_NDM_x.4_NDM19_NDM22', 'AMR_NDM_x.4_NDM19_NDM22',
        'AMR_NDM_x.7_NDM33_NDM36', 'AMR_NDM_x.7_NDM33_NDM36',
        'AMR_NDM_x.7_NDM33_NDM36', 'AMR_NDM_x.7_NDM33_NDM36',
        'AMR_NDM_x.7_NDM33_NDM36', 'AMR_NDM_x.7_NDM33_NDM36', '', ''
        ],
    'PA Primers': [
        'AMR_NDM_6.x_NDM17_NDM23', 'AMR_NDM_6.x_NDM17_NDM23',
        'AMR_NDM_5.x_NDM17_NDM24', 'AMR_NDM_5.x_NDM17_NDM24',
        'AMR_NDM_9.x_NDM31_NDM38', 'AMR_NDM_9.x_NDM31_NDM38',
        'AMR_NDM_10.x_NDM31_NDM39', 'AMR_NDM_10.x_NDM31_NDM39',
        'AMR_NDM_11.x_NDM32_NDM38', 'AMR_NDM_11.x_NDM32_NDM38', '', ''
    ],
    'Template': [
        'K.pneumoniae-NDM_2146', 'K.pneumoniae-NDM_2146',
        'K.pneumoniae-NDM_2146', 'K.pneumoniae-NDM_2146',
        'K.pneumoniae-NDM_2146', 'K.pneumoniae-NDM_2146',
        'K.pneumoniae-NDM_2146', 'K.pneumoniae-NDM_2146',
        'K.pneumoniae-NDM_2146', 'K.pneumoniae-NDM_2146', '', ''
    ]
}

def get_allocated_cols(allocation):
    allocated_cols = {}
    for reagent_class, reagents in allocation.items():
        allocated_cols[reagent_class] = \
            [i for i, r in enumerate(reagents, 1) if r]
    first = list(allocated_cols.values())[0]
    if all(v == first for v in allocated_cols.values()):
        return first
    else:
        raise ValueError('One of {} is missing values'.format(
            list(allocated_cols.keys())))


def reduce_cols(cols):
    if len(cols) == cols[-1]:
        return '{}-{}'.format(cols[0], cols[-1])
    else:
        raise ValueError('Rows not reducible')

def reduce_rows(rows):
    if len(rows) == ord(rows[-1]) - 64:
        return '{}-{}'.format(rows[0], rows[-1])
    else:
        raise ValueError('Columns not reducible')

def make_mastermix_dsl(mastermix, allocated_cols, allocated_rows=PLATE_ROWS):

    cols = reduce_cols(allocated_cols)
    rows = reduce_rows(allocated_rows)

    mastermix_dsl = []
    mastermix = get_mastermix(mastermix)
    for reagent in mastermix:
        line = [reagent['name'], cols, rows, str(reagent['quantity']),
                reagent['unit']]
        mastermix_dsl.append(' '.join(line))
    return '\n'.join(mastermix_dsl)

print(make_mastermix_dsl('pa mastermix A', get_allocated_cols(ALLOCATION)))

def make_nested_dsl(allocation):
    allocated_cols = get_allocated_cols(allocation)

