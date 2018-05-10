
from typing import Dict

from clients.expt_recipes.vanilla.models import IdConstituents
from hardware.plates import WellName

Constituents = Dict[WellName, IdConstituents]


def get_wells_by_id_assay(id_qpcr_constituents: Constituents):
    """
    Creates a dictionary keyed by id assay and valued by associated well names.
    :param id_qpcr_constituents: a dictionary keyed by well name and valued by
    instances of `IdConstituents`
    :return:
    """
    groupings = create_vanilla_grouping(id_qpcr_constituents)

    wells_by_id_assay = {}
    for id_assay in groupings:
        wells_by_id_assay[id_assay] = []
        for template in groupings[id_assay]:
            wells_by_id_assay[id_assay] = \
                wells_by_id_assay[id_assay] + list(
                    groupings[id_assay][template].keys())
    return wells_by_id_assay


def create_vanilla_grouping(id_qpcr_constituents):
    groups = {}
    idgrp = group_by_id_assay(id_qpcr_constituents)
    for id_assay, id_constits in idgrp.items():
        groups[id_assay] = {}
        tgrp = group_by_template_origin(id_constits)
        for t, t_constituents in tgrp.items():
            groups[id_assay][t] = t_constituents
    return groups


def group_by_id_assay(constituents: Constituents):
    """
    Groups constituents by id assay.
    :param constituents: a dictionary keyed by well name and valued by
    instances of `IdQpcrData`
    :return:
    """
    wells_by_id_assay = {}
    for w, c in constituents.items():
        id_assay = c.get_id_assay_attribute('reagent_name')
        inner = wells_by_id_assay.setdefault(id_assay, {})
        inner[w] = c
    return wells_by_id_assay


def group_by_template_origin(constituents: Constituents):
    """
    Groups constituents by template origin.
    :param constituents: a dictionary keyed by well name and valued by
    instances of `IdQpcrData`
    :return:
    """
    wells_by_template = {}
    for w, c in constituents.items():
        id_template = c.get_id_template_attribute('reagent_name')
        if id_template:
            inner = wells_by_template.setdefault('id', {})
        else:
            inner = wells_by_template.setdefault('NTC', {})
        inner[w] = c
    return wells_by_template
