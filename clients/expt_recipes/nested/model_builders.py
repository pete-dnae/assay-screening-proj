import re
from typing import Dict

from clients.transfers import get_parent_wells, get_dilutions
from clients.expt_recipes.nested.models import NestedIdWellConstituents, \
    NestedIdQpcrData, NestedLabChipData
from clients.expt_recipes.results_interpretation.constituents import \
    get_ntc_wells
from hardware.plates import ExptPlates, WellName, Plate
import hardware.qpcr as hwq

GroupedConstituents = Dict[WellName, NestedIdWellConstituents]


def build_id_qpcr_datas_from_inst_data(
        id_plate_constituents: GroupedConstituents,
        raw_instrument_data: hwq.qPCRInstPlate):
    """
    Creates a dictionary keyed by well names and valued by instances of
    `NestedIdQpcrData`.

    Iterates over all the wells in a plates and initially groups them by the
    id assay and then the preamp assay. At various stages in the grouping
    process, intermediate values are calculated as they are required when
    creating a `NestedIdQpcrData`.

    :param id_plate_constituents: a dictionary keyed by well name and valued by
    instances of `NestedIdWellConstituents`
    :param raw_instrument_data: the python representation of qPCR results for
    the well in question
    :return:
    """
    id_qpcr_datas = {}
    id_grouped = group_by_id_assay(id_plate_constituents)
    for id_assay, id_constits in id_grouped.items():
        max_conc_mean_tm = \
            calc_max_conc_mean_tm(id_constits, raw_instrument_data)
        pa_grouped = group_by_pa_assay(id_constits)
        for pa_assay, pa_constits in pa_grouped.items():
            mean_ntc_ct = calc_mean_ntc_ct(pa_constits, raw_instrument_data)
            for w, nic in pa_constits.items():
                well_data = raw_instrument_data[w]
                id_qpcr_datas[w] = \
                    NestedIdQpcrData.create_from_inst_data(well_data,
                                                           max_conc_mean_tm,
                                                           mean_ntc_ct)
    return id_qpcr_datas


def build_id_qpcr_constituents(id_plate: Plate, all_expt_plates: ExptPlates) \
        -> GroupedConstituents:
    """
    Builds a dictionary keyed by the well names. The values are instances of
    `NestedIdWellConstituents`
    :param id_plate: a dictionary keyed by well name and valued by instances
    of `NestedIdWellConstituents`
    :param all_expt_plates: an instance of ExptPlates for this particular
    experiment
    :return:
    """
    id_qpcr_constituents = {}
    for w, reagents in id_plate.items():
        id_qpcr_constituents[w] = \
            NestedIdWellConstituents.create(reagents, all_expt_plates)
    return id_qpcr_constituents


def get_id_qpcr_plate_names(all_expt_plates: ExptPlates):
    """
    Extracts those plates in a nested experiment which are the id plates.
    :param all_expt_plates: all plates used for an experiment
    :return:
    """
    id_plate_names = [p for p in all_expt_plates if p.endswith('_ID')]
    if not id_plate_names:
        raise ValueError('No id plates detected.')
    else:
        return id_plate_names


def create_nested_groupings(id_plate: GroupedConstituents):
    """
    Group nested wells based upon their constituents.
    :param id_plate: a dictionary keyed by well name and valued by instances
    of `NestedIdWellConstituents`
    :return:
    """
    groups = {}
    idgrp = group_by_id_assay(id_plate)
    for id_assay, id_constits in idgrp.items():
        groups[id_assay] = {}
        pagrp = group_by_pa_assay(id_constits)
        for pa_assay, pa_constits in pagrp.items():
            groups[id_assay][pa_assay] = {}
            tgrp = group_by_template_origin(pa_constits)
            for t, t_constituents in tgrp.items():
                groups[id_assay][pa_assay][t] = t_constituents
    return groups


def group_by_id_assay(constituents: GroupedConstituents):
    """
    Groups constituents by id assay.
    :param constituents: a dictionary keyed by well name and valued by
    instances of `NestedIdQpcrData`
    :return:
    """
    wells_by_id_assay = {}
    for w, c in constituents.items():
        id_assay = c.get_id_assay_attribute('reagent_name')
        inner = wells_by_id_assay.setdefault(id_assay, {})
        inner[w] = c
    return wells_by_id_assay


def group_by_pa_assay(constituents: GroupedConstituents):
    """
    Groups constituents by pa assay.
    :param constituents: a dictionary keyed by well name and valued by
    instances of `NestedIdQpcrData`
    :return:
    """
    wells_by_pa_assay = {}
    for w, c in constituents.items():
        pa_assay = c.get_pa_assay_attribute('reagent_name')
        inner = wells_by_pa_assay.setdefault(pa_assay, {})
        inner[w] = c
    return wells_by_pa_assay


def group_by_template_origin(constituents: GroupedConstituents):
    """
    Groups constituents by template origin.
    :param constituents: a dictionary keyed by well name and valued by
    instances of `NestedIdQpcrData`
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


def calc_max_conc_mean_tm(constituents: GroupedConstituents,
                          raw_instrument_data: hwq.qPCRInstPlate):
    """
    Calculates the melting temperature ("tm") for the wells that have
    the maximum concentration of template.

    For nested experiments, these are exclusively the id only template wells.

    :param constituents: a dictionary keyed by well name and valued by instances
    of `NestedIdWellConstituents`
    :param raw_instrument_data:
    :return:
    """
    id_template_only_wells = get_id_template_only_wells(constituents)
    max_conc_wells = get_max_conc_template_from_id_wells(id_template_only_wells)
    qpcr_datas = [raw_instrument_data[w] for w in max_conc_wells]
    max_conc_mean_tm = hwq.calc_mean_tm(qpcr_datas)
    return max_conc_mean_tm


def calc_mean_ntc_ct(constituents: GroupedConstituents,
                     raw_instrument_data: hwq.qPCRInstPlate):
    ntc_wells = get_ntc_wells(constituents)
    qpcr_datas = [raw_instrument_data[w] for w in ntc_wells]
    mean_ntc_ct = hwq.get_mean_ct(qpcr_datas)
    return mean_ntc_ct


def get_id_template_only_wells(constituents: GroupedConstituents):
    """
    Gets a dictionary of those wells which only contain template introduced
    at the id stage.

    :param constituents: a dictionary keyed by id assay and valued by instances
    of `NestedIdQpcrData`
    :return:
    """
    id_template_only_wells = {}
    for w, c in constituents.items():
        if not c.get_pa_template_attribute('reagent_name') and \
                c.get_id_template_attribute('reagent_name'):
            id_template_only_wells[w] = c
    return id_template_only_wells


def get_max_conc_template_from_id_wells(
        id_template_only_wells: GroupedConstituents):
    """
    Get from the id wells, those wells that have the highest template
    concentration.

    :param id_template_only_wells: a dictionary keyed by well name and valued
    by instances of `NestedIdWellConstituents`
    :return:
    """
    concs = dict((w, wc.get_id_template_attribute('concentration'))
                 for w, wc in id_template_only_wells.items())
    max_conc = max(concs.values())

    max_conc_wells = {}
    for w, wc in id_template_only_wells.items():
        if concs[w] == max_conc:
            max_conc_wells[w] = wc
    return max_conc_wells


def get_labchip_plate_names(all_expt_plates: ExptPlates):
    """
    Extracts those plates in a nested experiment which are the labchip plates.
    :param all_expt_plates: all plates used for an experiment
    :return:
    """
    lc_plate_names = []
    for p in all_expt_plates:
        searched = re.search('\d{8}_\w', p)
        if searched:
            lc_plate_names.append(searched.group())
    if not lc_plate_names:
        raise ValueError('No LabChip plates detected!')
    else:
        return lc_plate_names


def create_id_qpcr_lc_mapping(lc_plate_data, lc_plate_name):
    id_qpcr_lc_mapping = {}
    for lcw, reagents in lc_plate_data.items():
        parents = get_parent_wells(reagents)
        if len(parents) > 1:
            raise ValueError('Labchip well {} has more than one parent '
                             'qpcr well'.format(lcw))
        idp, idw = parents[0]
        inner = id_qpcr_lc_mapping.setdefault(idp, {})
        inner[idw] = (lc_plate_name, lcw)
    return id_qpcr_lc_mapping


def get_lc_dilutions(lc_plate):
    lc_dilutions = {}
    for w, reagents in lc_plate.items():
        dilutions = get_dilutions(reagents)
        if len(dilutions) > 1:
            raise ValueError('Labchip well {} has more than one parent '
                             'qpcr well'.format(w))
        lc_dilutions[w] = dilutions[0]
    return lc_dilutions


def build_labchip_results_by_id_well(id_plate_constituents, lc_data_wells,
                                     mapping, assays, dilutions):
    lc_plate_results = {}
    for idw, constits in id_plate_constituents.items():
        lcp, lcw = mapping[idw]
        ass = constits.get_id_assay_attribute('reagent_name')
        lc_plate_results[idw] = \
            NestedLabChipData.create_from_inst_data(lc_data_wells[lcw],
                                                    [assays[a] for a in ass],
                                                    dilutions[lcw])
    return lc_plate_results
