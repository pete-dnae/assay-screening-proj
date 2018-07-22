
import re
from itertools import groupby

from app.mob2dsl.mastermix import get_mastermix
from app.mob2dsl.sample_layout import get_sample_layout

PLATE_COLS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
PLATE_ROWS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

DSL_NAME = 1
DSL_COL = 2
DSL_ROW = 3
DSL_CONC = 4
DSL_UNIT = 5


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
    ],
    'Human': ['HgDNA_Promega305466', 'HgDNA_Promega305466',
              'HgDNA_Promega305466', 'HgDNA_Promega305466',
              'HgDNA_Promega305466', 'HgDNA_Promega305466',
              'HgDNA_Promega305466', 'HgDNA_Promega305466',
              'HgDNA_Promega305466', 'HgDNA_Promega305466', '', '']
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


def consecutive(items):
    if items == list(range(min(items), max(items) + 1)):
        return True
    else:
        return False


def consecutive_rows(rows):
    return consecutive([ord(r) for r in rows])


def consecutive_cols(cols):
    return consecutive(cols)


def collapse_cols(cols):
    cols = sorted([int(c) for c in cols])
    if consecutive_cols(cols):
        return '{}-{}'.format(cols[0], cols[-1])
    else:
        return ','.join([str(c) for c in cols])


def collapse_rows(rows):
    rows = sorted(rows)
    if consecutive_rows(rows):
        return '{}-{}'.format(rows[0], rows[-1])
    else:
        return ','.join(rows)


def make_dsl_line(name, cols, rows, quantity, unit):
    if type(quantity) != str:
        quantity = '{:.3f}'.format(quantity)
    line = 'A {} {} {} {} {}'.format(name, cols, rows, quantity, unit)
    return line


def collapse_dsl_lines(lines):
    # Get all unique reagent names
    reagents = list(set([line.split()[DSL_NAME] for line in lines]))
    collapsed_lines = []
    for r in reagents:
        # extract out lines that match reagent
        matches = [line for line in lines if line.split()[DSL_NAME] == r]
        # Sort them by concentration
        matches = sorted(matches, key=lambda x: x.split()[DSL_CONC])

        # Group them by concentration
        for conc, grp in groupby(matches, lambda x: x.split()[DSL_CONC]):
            grp = list(grp)
            cols = collapse_cols(set(line.split()[DSL_COL] for line in grp))
            rows = collapse_rows(set(line.split()[DSL_ROW] for line in grp))

            unit = list(set(line.split()[DSL_UNIT] for line in matches))
            if len(unit) != 1:
                raise ValueError('Could not determine unit for {}'.format(r))

            collapsed_lines.append(make_dsl_line(r, cols, rows,
                                                 conc, unit[0]))
    return collapsed_lines


def make_mastermix_dsl(mastermix, cols, rows=PLATE_ROWS):

    dsl_lines = []
    mastermix = get_mastermix(mastermix)
    for reagent in mastermix:
        for r in rows:
            for c in cols:
                line = make_dsl_line(reagent['name'], c, r,
                                     reagent['quantity'], reagent['unit'])
                dsl_lines.append(line)
    return dsl_lines


def group_by_common_reagent(reagents):
    grps = {r: set() for r in set(reagents)}
    for i, r in enumerate(reagents, 1):
        grps[r].add(i)
    return grps


def make_assay_dsl(assays, primer_conc, primer_unit,
                   rows):
    # Group by common assays and get their column numbers
    grps = group_by_common_reagent(assays)

    assay_dsl = []
    for a, cols in grps.items():
        if a:
            for r in rows:
                for c in cols:
                    line = make_dsl_line(a, c, r, primer_conc, primer_unit)
                    assay_dsl.append(line)
    return assay_dsl


def make_template_dsl(templates, template_layout, rows):
    grps = group_by_common_reagent(templates)
    templates_dsl = []
    for t, cols in grps.items():
        if t:
            for r in rows:
                for c in cols:
                    well = '{}{:02d}'.format(r, c)
                    conc, unit = re.search('(\d+)(.*)',
                                           template_layout[well]).groups()
                    line = make_dsl_line(t, c, r, conc, unit)
                    templates_dsl.append(line)
    return templates_dsl


def make_human_dsl(humans, human_layout, rows):
    grps = group_by_common_reagent(humans)
    human_dsl = []
    for h, cols in grps.items():
        if h:
            for r in rows:
                for c in cols:
                    well = '{}{:02d}'.format(r, c)
                    conc, unit = re.search('(\d+)(.*)',
                                           human_layout[well]).groups()
                    line = make_dsl_line(h, c, r, conc, unit)
                    human_dsl.append(line)
    return human_dsl


def make_nested_pa_dsl(allocation):
    allocated_cols = get_allocated_cols(allocation)

    pa_mastermix_dsl = collapse_dsl_lines(
        make_mastermix_dsl('pa mastermix A', allocated_cols))

    pa_assays_dsl = collapse_dsl_lines(
        make_assay_dsl(allocation['PA Primers'], PA_PRIMERS_CONC,
                       PA_PRIMERS_UNIT, PLATE_ROWS))
    # sort by columns
    pa_assays_dsl = sorted(pa_assays_dsl, key=lambda x: x.split()[DSL_COL])

    sample_layout = get_sample_layout(SAMPLE_LAYOUT)

    template_layout = {k: v['template'] for k, v in sample_layout.items()}
    template_rows = sorted(set(k[0] for k, v in template_layout.items()
                               if v != '0cp'))
    template_dsl = collapse_dsl_lines(
        make_template_dsl(allocation['Template'], template_layout,
                          template_rows))

    human_layout = {k: v['human'] for k, v in sample_layout.items()}
    human_rows = sorted(set(k[0] for k, v in human_layout.items()
                            if v != '0ng'))
    human_dsl = collapse_dsl_lines(
        make_human_dsl(allocation['Human'], human_layout, human_rows))

    pa_dsl = pa_mastermix_dsl + pa_assays_dsl + template_dsl + human_dsl

    return '\n'.join(pa_dsl)


# print(make_nested_pa_dsl(ALLOCATION))


def make_nested_id_dsl(allocation):
    allocated_cols = get_allocated_cols(allocation)

    id_mastermix_dsl = collapse_dsl_lines(
        make_mastermix_dsl('id mastermix A', allocated_cols))

    id_assays_dsl = collapse_dsl_lines(
        make_assay_dsl(allocation['ID Primers'], PA_PRIMERS_CONC,
                       PA_PRIMERS_UNIT, PLATE_ROWS))
    # sort by columns
    id_assays_dsl = sorted(id_assays_dsl, key=lambda x: x.split()[DSL_COL])

    sample_layout = get_sample_layout(SAMPLE_LAYOUT)

    template_layout = {k: v['template'] for k, v in sample_layout.items()}
    template_rows = sorted(set(k[0] for k, v in template_layout.items()
                               if v != '0cp'))
    template_dsl = collapse_dsl_lines(
        make_template_dsl(allocation['Template'], template_layout,
                          template_rows))

    human_layout = {k: v['human'] for k, v in sample_layout.items()}
    human_rows = sorted(set(k[0] for k, v in human_layout.items()
                            if v != '0ng'))
    human_dsl = collapse_dsl_lines(
        make_human_dsl(allocation['Human'], human_layout, human_rows))

    id_dsl = id_mastermix_dsl + id_assays_dsl + template_dsl + human_dsl

    return '\n'.join(id_dsl)


# TODO: Need to take account of transfers
print(make_nested_id_dsl(ALLOCATION))
