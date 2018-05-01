
"""
This module is responsible for the construction of nested assay screening
experiments.
"""


from typing import List, Dict
from hardware.plates import WellName, Plate, ExptPlates
import re

from collections import OrderedDict

from clients.reagents import ObjReagent
from clients.reagents import get_assays, get_templates, disambiguate_templates
from clients.transfers import get_transferred_assays, get_transferred_templates

from clients.expt_recipes.well_constituents import WellConstituents
from clients.expt_recipes.results_interpretation.constituents import \
    get_ntc_wells
from clients.expt_recipes.results_interpretation.qpcr import get_mean_ct, \
    calc_delta_ct, get_ct_call, calc_mean_tm, get_product_labels_from_tms
from hardware.qpcr import get_ct, get_tms, calc_tm_deltas


class NestedIdWellConstituents(WellConstituents):

    def __init__(self):
        super().__init__()

    @classmethod
    def create(cls, reagents: List[ObjReagent],
               all_expt_plates: ExptPlates) -> 'NestedIdWellConstituents':

        inst = cls()
        inst['assays'] = get_assays(reagents)
        inst['transferred_assays'] = \
            get_transferred_assays(reagents, all_expt_plates)
        inst['human'], inst['templates'] = \
            disambiguate_templates(get_templates(reagents))
        inst['transferred_human'], inst['transferred_templates'] = \
            disambiguate_templates(get_transferred_templates(reagents,
                                                             all_expt_plates))

        return inst

    def get_id_assay_attribute(self, attribute):
        return self._get_item_attribute('assays', attribute)

    def get_pa_assay_attribute(self, attribute):
        return self._get_item_attribute('transferred_assays', attribute)

    def get_id_template_attribute(self, attribute):
        return self._get_item_attribute('templates', attribute)

    def get_id_human_attribute(self, attribute):
        return self._get_item_attribute('human', attribute)

    def get_pa_template_attribute(self, attribute):
        return self._get_item_attribute('transferred_templates', attribute)

    def get_pa_human_attribute(self, attribute):
        return self._get_item_attribute('transferred_human', attribute)


class NestedIdQpcrData(OrderedDict):

    def __init__(self):
        super().__init__()
        self['Ct'] = None
        self['∆NTC_Ct'] = None
        self['Ct_Call'] = None
        self['Tm1'] = None
        self['Tm2'] = None
        self['Tm3'] = None
        self['Tm4'] = None
        self['Tm Specif'] = None
        self['Tm NS'] = None
        self['Tm PD'] = None

    @classmethod
    def create(cls, ct, delta_ct, ct_call, tms, spec, non_spec, pd) -> \
            'NestedIdQpcrData':
        inst = cls()
        inst['Ct'] = ct
        inst['∆NTC_Ct'] = delta_ct
        inst['Ct_Call'] = ct_call
        inst['Tm1'] = tms[0]
        inst['Tm2'] = tms[1]
        inst['Tm3'] = tms[2]
        inst['Tm4'] = tms[3]
        inst['Tm Specif'] = spec
        inst['Tm NS'] = non_spec
        inst['Tm PD'] = pd

        return inst

    @classmethod
    def create_from_data(cls, well_name, raw_instrument_data, max_conc_mean_tm,
                         mean_ntc_ct) -> 'NestedIdQpcrData':

        tms = get_tms(raw_instrument_data[well_name])
        tm_delta = calc_tm_deltas(raw_instrument_data[well_name],
                                  max_conc_mean_tm)
        ct = get_ct(raw_instrument_data[well_name])
        delta_ct = calc_delta_ct(ct, mean_ntc_ct)
        ct_call = get_ct_call(delta_ct)
        spec, non_spec, pd = get_product_labels_from_tms(tms, tm_delta,
                                                         max_conc_mean_tm)
        inst = cls()
        nid = inst.create(ct, delta_ct, ct_call, tms, spec, non_spec, pd)
        return nid

    def is_populated(self):
        return all(v is not None for v in self.values())


class NestedLabChipData(OrderedDict):

    def __init__(self):
        super().__init__()
        self['Specif ng/ul'] = None
        self['NS ng/ul'] = None
        self['PD ng/ul'] = None

    @classmethod
    def create(cls, spec, non_spec, pd):
        inst = cls()
        inst['Specif ng/ul'] = spec
        inst['NS ng/ul'] = non_spec
        inst['PD ng/ul'] = pd

    @classmethod
    def create_from_data(cls):
        return


def get_id_plates(all_expt_plates: ExptPlates):
    """
    Extracts those plates in a nested experiment which are the id plates.
    :param all_expt_plates: all plates used for an experiment
    :return:
    """
    id_plate_names = [p for p in all_expt_plates if p.endswith('_ID')]
    return id_plate_names


GroupedConstituents = Dict[WellName, NestedIdWellConstituents]


def build_constituents(id_plate: Plate, all_expt_plates: ExptPlates) \
        -> GroupedConstituents:
    """
    Builds a dictionary keyed by the well names. The values are instances of
    `NestedIdWellConstituents`
    :param id_plate:  a dictionary keyed by well name and valued by instances
    of `NestedIdWellConstituents`
    :param all_expt_plates: an instance of ExptPlates for this particular
    experiment
    :return:
    """
    well_constituents = {}
    for w, reagents in id_plate.items():
        well_constituents[w] = \
            NestedIdWellConstituents.create(reagents, all_expt_plates)
    return well_constituents


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


def build_qpcr_datas(id_plate: GroupedConstituents, raw_instrument_data):
    """
    Creates a dictionary keyed by well names and valued by instances of
    `NestedIdQpcrData`.

    Iterates over all the wells in a plates and initially groups them by the
    id assay and then the preamp assay. At various stages in the grouping
    process, intermediate values are calculated as they are required when
    creating a `NestedIdQpcrData`.

    :param id_plate: a dictionary keyed by well name and valued by instances
    of `NestedIdWellConstituents`
    :param raw_instrument_data: the python representation of qPCR results for
    the well in question
    :return:
    """
    nested_id_datas = {}
    id_grouped = group_by_id_assay(id_plate)
    for id_assay, id_constits in id_grouped.items():
        max_conc_mean_tm = \
            calc_max_conc_mean_tm(id_constits, raw_instrument_data)
        pa_grouped = group_by_pa_assay(id_constits)
        for pa_assay, pa_constits in pa_grouped.items():
            ntc_wells = get_ntc_wells(pa_constits)
            mean_ntc_ct = get_mean_ct(list(ntc_wells.keys()),
                                      raw_instrument_data)
            for w, nic in pa_constits.items():
                nested_id_datas[w] = \
                    NestedIdQpcrData.create_from_data(w, raw_instrument_data,
                                                      max_conc_mean_tm,
                                                      mean_ntc_ct)
    return nested_id_datas


def calc_max_conc_mean_tm(constituents: GroupedConstituents,
                          raw_instrument_data):
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
    max_conc_mean_tm = calc_mean_tm(list(max_conc_wells.keys()),
                                    raw_instrument_data)
    return max_conc_mean_tm


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

def get_labchip_plates(all_expt_plates: ExptPlates):
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
    return lc_plate_names
