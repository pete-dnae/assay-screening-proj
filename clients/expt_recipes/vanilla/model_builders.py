

from clients.expt_recipes.common.models import IdQpcrData
from clients.expt_recipes.common.utils import get_ntc_wells
from clients.expt_recipes.interp.qpcr import default_ct_if_nan
from hardware.qpcr import get_mean_ct, calc_mean_tm


def build_id_qpcr_datas_from_inst_data(id_qconsts, qinst_plate):
    """
    Creates a dictionary keyed by well names and valued by instances of
    `IdQpcrData`.

    Iterates over all the wells in a plate and initially groups them by the
    id assay. At various stages in the grouping process, intermediate values
    are calculated as they are required when creating a `IdQpcrData`.

    :param id_qconsts: a dictionary of wells containing constituents
    :param qinst_plate: a dictionary of wells containing instrument data
    :return:
    """
    id_qpcr_datas = {}
    id_grouped = _group_by_id_assay(id_qconsts)
    for id_assay, id_constits in id_grouped.items():
        max_conc_mean_tm = _calc_max_conc_mean_tm(id_constits, qinst_plate)

        ntc_wells = get_ntc_wells(id_constits)
        qpcr_datas = [qinst_plate[w] for w in ntc_wells]
        mean_ntc_ct = default_ct_if_nan(get_mean_ct(qpcr_datas))

        for w, nic in id_constits.items():
            well_data = qinst_plate[w]
            id_qpcr_datas[w] = \
                IdQpcrData.create_from_inst_data(well_data,
                                                 max_conc_mean_tm,
                                                 mean_ntc_ct)
    return id_qpcr_datas


def _get_wells_by_id_assay(id_qconsts):
    """
    Creates a dictionary keyed by id assay and valued by associated well names.
    :param id_qconsts: a dictionary of wells containing constituents
    :return:
    """
    groupings = _create_vanilla_groupings(id_qconsts)

    wells_by_id_assay = {}
    for id_assay in groupings:
        wells_by_id_assay[id_assay] = []
        for template in groupings[id_assay]:
            wells_by_id_assay[id_assay] = \
                wells_by_id_assay[id_assay] + list(
                    groupings[id_assay][template].keys())
    return wells_by_id_assay


def _create_vanilla_groupings(id_qconsts):
    """
    Groups wells into a nested dictionary according to the "vanilla" grouping
    pattern of:
    id assay -> template

    :param id_qconsts: a dictionary of wells containing constituents
    :return:
    """
    groups = {}
    idgrp = _group_by_id_assay(id_qconsts)
    for id_assay, id_constits in idgrp.items():
        groups[id_assay] = {}
        tgrp = _group_by_template_origin(id_constits)
        for t, t_constituents in tgrp.items():
            groups[id_assay][t] = t_constituents
    return groups


def _group_by_id_assay(id_qconsts):
    """
    Groups constituents by id assay.
    :param id_qconsts: a dictionary of wells containing constituents
    :return:
    """
    wells_by_id_assay = {}
    for w, c in id_qconsts.items():
        id_assay = c.get_id_assay_attribute('reagent_name')
        inner = wells_by_id_assay.setdefault(id_assay, {})
        inner[w] = c
    return wells_by_id_assay


def _group_by_template_origin(id_qconsts):
    """
    Groups constituents by template origin.
    :param id_qconsts: a dictionary of wells containing constituents
    :return:
    """
    wells_by_template = {}
    for w, c in id_qconsts.items():
        id_template = c.get_id_template_attribute('reagent_name')
        if id_template:
            inner = wells_by_template.setdefault('id', {})
        else:
            inner = wells_by_template.setdefault('NTC', {})
        inner[w] = c
    return wells_by_template


def _calc_max_conc_mean_tm(id_qconsts, qinst_data):
    """
    Calculates the melting temperature ("tm") for the wells that have
    the maximum concentration of template.

    For nested experiments, these are exclusively the id only template wells.

    :param id_qconsts: a dictionary of wells containing constituents
    :param qinst_data: qPCR instrument data
    :return:
    """
    max_conc_wells = _get_max_conc_template_from_id_wells(id_qconsts)
    qpcr_datas = [qinst_data[w] for w in max_conc_wells]
    max_conc_mean_tm = calc_mean_tm(qpcr_datas)
    return max_conc_mean_tm


def _get_max_conc_template_from_id_wells(id_qconsts):
    """
    Get from the id wells, those wells that have the highest template
    concentration.

    :param id_qconsts: a dictionary of wells containing constituents
    :return:
    """
    concs = dict((w, wc.get_id_template_attribute('concentration'))
                 for w, wc in id_qconsts.items())
    max_conc = max(concs.values())

    max_conc_wells = {}
    for w, c in id_qconsts.items():
        if concs[w] == max_conc:
            max_conc_wells[w] = c
    return max_conc_wells
