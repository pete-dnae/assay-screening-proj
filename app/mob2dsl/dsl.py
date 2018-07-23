
import re
from itertools import groupby

PLATE_ROWS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
from app.mob2dsl.mastermix import get_mastermix


DSL_NAME = 1
DSL_COL = 2
DSL_ROW = 3
DSL_CONC = 4
DSL_UNIT = 5


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
            cols = _collapse_cols(set(line.split()[DSL_COL] for line in grp))
            rows = _collapse_rows(set(line.split()[DSL_ROW] for line in grp))

            unit = list(set(line.split()[DSL_UNIT] for line in matches))
            if len(unit) != 1:
                raise ValueError('Could not determine unit for {}'.format(r))

            collapsed_lines.append(_make_allocate_line(r, cols, rows,
                                                       conc, unit[0]))
    # sort by columns
    collapsed_lines = sorted(collapsed_lines, key=lambda x: x.split()[DSL_COL])
    return collapsed_lines


def make_mastermix_dsl(mastermix, cols, rows=PLATE_ROWS):

    dsl_lines = []
    mastermix = get_mastermix(mastermix)
    for reagent in mastermix:
        for r in rows:
            for c in cols:
                line = _make_allocate_line(reagent['name'], c, r,
                                           reagent['quantity'], reagent['unit'])
                dsl_lines.append(line)
    return dsl_lines


def make_assay_dsl(assays, primer_conc, primer_unit,
                   rows):
    # Group by common assays and get their column numbers
    grps = _group_by_common_reagent(assays)
    assay_dsl = []
    for a, cols in grps.items():
        if a:
            for r in rows:
                for c in cols:
                    line = _make_allocate_line(a, c, r, primer_conc, primer_unit)
                    assay_dsl.append(line)
    return assay_dsl


def make_template_dsl(templates, template_layout, rows):
    grps = _group_by_common_reagent(templates)
    templates_dsl = []
    for t, cols in grps.items():
        if t:
            for r in rows:
                for c in cols:
                    well = '{}{:02d}'.format(r, c)
                    conc, unit = re.search('(\d+)(.*)',
                                           template_layout[well]).groups()
                    line = _make_allocate_line(t, c, r, conc, unit)
                    templates_dsl.append(line)
    return templates_dsl


def make_human_dsl(humans, human_layout, rows):
    grps = _group_by_common_reagent(humans)
    human_dsl = []
    for h, cols in grps.items():
        if h:
            for r in rows:
                for c in cols:
                    well = '{}{:02d}'.format(r, c)
                    conc, unit = re.search('(\d+)(.*)',
                                           human_layout[well]).groups()
                    line = _make_allocate_line(h, c, r, conc, unit)
                    human_dsl.append(line)
    return human_dsl


def make_block_transfer(plate_id, rows, cols, dilution):
    rows = '{}-{}'.format(rows[0], rows[-1])
    cols = '{}-{}'.format(cols[0], cols[-1])
    line = 'T {} {} {} {} {} {}'.format(plate_id, cols, rows, cols, rows,
                                        dilution)
    return [line]


def _make_allocate_line(name, cols, rows, quantity, unit):
    if type(quantity) != str:
        quantity = '{:.3f}'.format(quantity)
    line = 'A {} {} {} {} {}'.format(name, cols, rows, quantity, unit)
    return line


def _group_by_common_reagent(reagents):
    grps = {r: set() for r in set(reagents.values())}
    for i, r in reagents.items():
        grps[r].add(i)
    return grps


def _consecutive(items):
    if items == list(range(min(items), max(items) + 1)):
        return True
    else:
        return False


def _consecutive_cols(cols):
    return _consecutive(cols)


def _collapse_cols(cols):
    cols = sorted([int(c) for c in cols])
    if _consecutive_cols(cols):
        return '{}-{}'.format(cols[0], cols[-1])
    else:
        return ','.join([str(c) for c in cols])


def _consecutive_rows(rows):
    return _consecutive([ord(r) for r in rows])


def _collapse_rows(rows):
    rows = sorted(rows)
    if _consecutive_rows(rows):
        return '{}-{}'.format(rows[0], rows[-1])
    else:
        return ','.join(rows)
