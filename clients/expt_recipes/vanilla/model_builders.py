
from typing import Dict

from clients.expt_recipes.common.models import IdQpcrData, LabChipData, \
    LabChipDatas, qPCRDatas
import clients.expt_recipes.interp.constituents as intc
from clients.expt_recipes.vanilla.models import IdConstituents
from hardware.plates import WellName
import hardware.qpcr as hwq
import hardware.labchip as hwlc

Constituents = Dict[WellName, IdConstituents]


def build_id_qpcr_datas_from_inst_data(
        id_qpcr_constituents: Constituents,
        instrument_data: hwq.qPCRInstPlate) -> qPCRDatas:
    """
    Creates a dictionary keyed by well names and valued by instances of
    `IdQpcrData`.

    Iterates over all the wells in a plates and initially groups them by the
    id assay and then the preamp assay. At various stages in the grouping
    process, intermediate values are calculated as they are required when
    creating a `IdQpcrData`.

    :param id_qpcr_constituents: a dictionary keyed by well name and valued by
    instances of `IdConstituents`
    :param instrument_data: the python representation of qPCR results for
    the well in question
    :return:
    """
    id_qpcr_datas = {}
    id_grouped = group_by_id_assay(id_qpcr_constituents)
    for id_assay, id_constits in id_grouped.items():
        max_conc_mean_tm = \
            calc_max_conc_mean_tm(id_constits, instrument_data)
        mean_ntc_ct = calc_mean_ntc_ct(id_constits, instrument_data)
        for w, nic in id_constits.items():
            well_data = instrument_data[w]
            id_qpcr_datas[w] = \
                IdQpcrData.create_from_inst_data(well_data,
                                                 max_conc_mean_tm,
                                                 mean_ntc_ct)
    return id_qpcr_datas


def get_wells_by_id_assay(id_qpcr_constituents: Constituents):
    """
    Creates a dictionary keyed by id assay and valued by associated well names.
    :param id_qpcr_constituents: a dictionary keyed by well name and valued by
    instances of `IdConstituents`
    :return:
    """
    groupings = create_vanilla_groupings(id_qpcr_constituents)

    wells_by_id_assay = {}
    for id_assay in groupings:
        wells_by_id_assay[id_assay] = []
        for template in groupings[id_assay]:
            wells_by_id_assay[id_assay] = \
                wells_by_id_assay[id_assay] + list(
                    groupings[id_assay][template].keys())
    return wells_by_id_assay


def create_vanilla_groupings(id_qpcr_constituents):
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


def calc_max_conc_mean_tm(constituents: Constituents,
                          instrument_data: hwq.qPCRInstPlate) -> float:
    """
    Calculates the melting temperature ("tm") for the wells that have
    the maximum concentration of template.

    For nested experiments, these are exclusively the id only template wells.

    :param constituents: a dictionary keyed by well name and valued by instances
    of `IdConstituents`
    :param instrument_data: qPCR instrument data
    :return:
    """
    max_conc_wells = get_max_conc_template_from_id_wells(constituents)
    qpcr_datas = [instrument_data[w] for w in max_conc_wells]
    max_conc_mean_tm = hwq.calc_mean_tm(qpcr_datas)
    return max_conc_mean_tm


def calc_mean_ntc_ct(constituents: Constituents,
                     raw_instrument_data: hwq.qPCRInstPlate) -> float:
    """

    :param constituents: a dictionary keyed by well name and valued by
    instances of `IdConstituents`
    :param raw_instrument_data: qPCR instrument data
    :return:
    """
    ntc_wells = intc.get_ntc_wells(constituents)
    qpcr_datas = [raw_instrument_data[w] for w in ntc_wells]
    mean_ntc_ct = hwq.get_mean_ct(qpcr_datas)
    return mean_ntc_ct


def get_max_conc_template_from_id_wells(
        constituents: Constituents) -> Constituents:
    """
    Get from the id wells, those wells that have the highest template
    concentration.

    :param constituents: a dictionary keyed by well name and valued
    by instances of `IdConstituents`
    :return:
    """
    concs = dict((w, wc.get_id_template_attribute('concentration'))
                 for w, wc in constituents.items())
    max_conc = max(concs.values())

    max_conc_wells = {}
    for w, c in constituents.items():
        if concs[w] == max_conc:
            max_conc_wells[w] = c
    return max_conc_wells
