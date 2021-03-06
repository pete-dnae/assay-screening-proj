
import re

from app.mob2dsl.dsl import collapse_dsl_lines, make_mastermix_dsl, \
    make_assay_dsl, make_template_dsl, make_human_dsl, make_block_transfer

from app.mob2dsl.user_input import TEMPLATE_HEADER, HUMAN_HEADER, \
    PA_PRIMER_HEADER, ID_PRIMER_HEADER


def make_nested_pa_dsl(plate, rows, cols, mastermix_version,
                       pa_primers_conc, pa_primers_unit, pa_layout):
    pa_mastermix_dsl = _make_mastermix_dsl(mastermix_version, rows, cols)
    pa_assays_dsl = _make_assay_dsl(plate, PA_PRIMER_HEADER, pa_primers_conc,
                                    pa_primers_unit, rows)
    template_dsl = _make_template_dsl(plate, pa_layout)
    human_dsl = _make_human_dsl(plate, pa_layout)
    return pa_mastermix_dsl + pa_assays_dsl + template_dsl + human_dsl


def make_nested_transfer_dsl(plate_id, rows, cols, dilution):
    transfer = make_block_transfer(plate_id, rows, cols, dilution)
    return transfer


def make_nested_id_dsl(plate, rows, cols, mastermix_version,
                       id_primers_conc, id_primers_unit, id_layout):

    id_mastermix_dsl = _make_mastermix_dsl(mastermix_version, rows, cols)
    id_assays_dsl = _make_assay_dsl(plate, ID_PRIMER_HEADER, id_primers_conc,
                                    id_primers_unit, rows)
    template_dsl = _make_template_dsl(plate, id_layout)
    human_dsl = _make_human_dsl(plate, id_layout)

    return id_mastermix_dsl + id_assays_dsl + template_dsl + human_dsl


def _make_mastermix_dsl(mastermix_version, rows, cols):
    mastermix_dsl = collapse_dsl_lines(
        make_mastermix_dsl(mastermix_version, rows, cols))
    return mastermix_dsl


def _make_assay_dsl(plate, primer_header, primer_conc, primer_unit, rows):
    assays_dsl = collapse_dsl_lines(
        make_assay_dsl(plate[primer_header], primer_conc,
                       primer_unit, rows))
    return assays_dsl


def _make_template_dsl(plate, layout):
    template_layout = {k: v[TEMPLATE_HEADER] for k, v in layout.items()}
    template_rows = sorted(set(k[0] for k, v in template_layout.items()
                               if not re.match('0cp', v)))
    template_dsl = collapse_dsl_lines(
        make_template_dsl(plate[TEMPLATE_HEADER], template_layout,
                          template_rows))
    return template_dsl


def _make_human_dsl(plate, layout):
    human_layout = {k: v[HUMAN_HEADER] for k, v in layout.items()}
    human_rows = sorted(set(k[0] for k, v in human_layout.items()
                            if not re.match('0[un]g', v)))
    human_dsl = collapse_dsl_lines(
        make_human_dsl(plate[HUMAN_HEADER], human_layout, human_rows))
    return human_dsl
