
from typing import Dict
from clients.expt_recipes.common.model_builders import calc_mean_ntc_ct
from clients.expt_recipes.common.models import WellName, IdQpcrData, qPCRDatas
from clients.expt_recipes.nested.models import IdConstituents
import hardware.qpcr as hwq

ConstituentsByWell = Dict[WellName, IdConstituents]


def build_id_qpcr_datas_from_inst_data(
        id_qpcr_constituents: ConstituentsByWell,
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
        pa_grouped = group_by_pa_assay(id_constits)
        for pa_assay, pa_constits in pa_grouped.items():
            mean_ntc_ct = calc_mean_ntc_ct(pa_constits, instrument_data)
            for w, nic in pa_constits.items():
                well_data = instrument_data[w]
                id_qpcr_datas[w] = \
                    IdQpcrData.create_from_inst_data(well_data,
                                                     max_conc_mean_tm,
                                                     mean_ntc_ct)
    return id_qpcr_datas


def get_wells_by_id_assay(id_qpcr_constituents: ConstituentsByWell):
    """
    Creates a dictionary keyed by id assay and valued by associated well names.
    :param id_qpcr_constituents: a dictionary keyed by well name and valued by
    instances of `IdConstituents`
    :return:
    """
    groupings = create_nested_groupings(id_qpcr_constituents)

    wells_by_id_assay = {}
    for id_assay in groupings:
        wells_by_id_assay[id_assay] = []
        for pa_assay in groupings[id_assay]:
            for template in groupings[id_assay][pa_assay]:
                wells_by_id_assay[id_assay] = \
                    wells_by_id_assay[id_assay] + list(
                        groupings[id_assay][pa_assay][template].keys())
    return wells_by_id_assay


def create_nested_groupings(id_qpcr_constituents: ConstituentsByWell):
    """
    Group nested wells based upon their constituents.
    :param id_qpcr_constituents: a dictionary keyed by well name and valued
    by instances of `IdConstituents`
    :return:
    """
    groups = {}
    idgrp = group_by_id_assay(id_qpcr_constituents)
    for id_assay, id_constits in idgrp.items():
        groups[id_assay] = {}
        pagrp = group_by_pa_assay(id_constits)
        for pa_assay, pa_constits in pagrp.items():
            groups[id_assay][pa_assay] = {}
            tgrp = group_by_template_origin(pa_constits)
            for t, t_constituents in tgrp.items():
                groups[id_assay][pa_assay][t] = t_constituents
    return groups


def group_by_id_assay(constituents: ConstituentsByWell):
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


def group_by_pa_assay(constituents: ConstituentsByWell):
    """
    Groups constituents by pa assay.
    :param constituents: a dictionary keyed by well name and valued by
    instances of `IdQpcrData`
    :return:
    """
    wells_by_pa_assay = {}
    for w, c in constituents.items():
        pa_assay = c.get_pa_assay_attribute('reagent_name')
        inner = wells_by_pa_assay.setdefault(pa_assay, {})
        inner[w] = c
    return wells_by_pa_assay


def group_by_template_origin(constituents: ConstituentsByWell):
    """
    Groups constituents by template origin.
    :param constituents: a dictionary keyed by well name and valued by
    instances of `IdQpcrData`
    :return:
    """
    wells_by_template = {}
    for w, c in constituents.items():
        pa_template = c.get_pa_template_attribute('reagent_name')
        id_template = c.get_id_template_attribute('reagent_name')
        if pa_template and not id_template:
            inner = wells_by_template.setdefault('preamp', {})
        elif id_template and not pa_template:
            inner = wells_by_template.setdefault('id', {})
        else:
            inner = wells_by_template.setdefault('NTC', {})
        inner[w] = c
    return wells_by_template


def calc_max_conc_mean_tm(constituents: ConstituentsByWell,
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
    id_template_only_wells = get_id_template_only_wells(constituents)
    max_conc_wells = get_max_conc_template_from_id_wells(id_template_only_wells)
    qpcr_datas = [instrument_data[w] for w in max_conc_wells]
    max_conc_mean_tm = hwq.calc_mean_tm(qpcr_datas)
    return max_conc_mean_tm


def get_id_template_only_wells(constituents: ConstituentsByWell) \
        -> ConstituentsByWell:
    """
    Gets a dictionary of those wells which only contain template introduced
    at the id stage.

    :param constituents: a dictionary keyed by id assay and valued by instances
    of `IdQpcrData`
    :return:
    """
    id_template_only_wells = {}
    for w, c in constituents.items():
        if not c.get_pa_template_attribute('reagent_name') and \
                c.get_id_template_attribute('reagent_name'):
            id_template_only_wells[w] = c
    return id_template_only_wells


def get_max_conc_template_from_id_wells(
        id_template_only_wells: ConstituentsByWell) -> ConstituentsByWell:
    """
    Get from the id wells, those wells that have the highest template
    concentration.

    :param id_template_only_wells: a dictionary keyed by well name and valued
    by instances of `IdConstituents`
    :return:
    """
    concs = dict((w, wc.get_id_template_attribute('concentration'))
                 for w, wc in id_template_only_wells.items())
    max_conc = max(concs.values())

    max_conc_wells = {}
    for w, c in id_template_only_wells.items():
        if concs[w] == max_conc:
            max_conc_wells[w] = c
    return max_conc_wells
