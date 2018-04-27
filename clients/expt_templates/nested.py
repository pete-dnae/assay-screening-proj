
from typing import List
from collections import OrderedDict

from clients.reagents import ObjReagent
from clients.reagents import get_assays, get_templates, disambiguate_templates
from clients.transfers import get_transferred_assays, get_transferred_templates
from hardware.plates import ExptPlates

from clients.expt_templates.well_contents import WellConstituents
from clients.expt_templates.results_interp import calc_mean_tm, get_tm_delta,\
    get_ntc_wells, get_mean_ct, get_delta_ct, get_ct, get_ct_call, get_tms, \
    get_product_labels_from_tms, SPECIFIC_PRODUCT, NON_SPECIFIC_PRODUCT, \
    PRIMER_DIMER


class NestedIdConstituents(WellConstituents):

    def __init__(self):
        super().__init__()

    @classmethod
    def create(cls, qpcr_well_id: str, reagents: List[ObjReagent],
               expt_plates: ExptPlates) -> 'NestedIdConstituents':

        inst = cls()
        inst['well_name'] = qpcr_well_id
        inst['assays'] = get_assays(reagents)
        inst['transferred_assays'] = \
            get_transferred_assays(reagents, expt_plates)
        inst['human'], inst['templates'] = \
            disambiguate_templates(get_templates(reagents))
        inst['transferred_human'], inst['transferred_templates'] = \
            disambiguate_templates(get_transferred_templates(reagents,
                                                             expt_plates))

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


class NestedIdData(OrderedDict):

    def __init__(self):
        super().__init__()
        self['well_name'] = None
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
    def create_from_data(cls, qpcr_well, ct, delta_ct, ct_call, tms, spec,
                         non_spec, pd) -> 'NestedIdData':
        inst = cls()
        inst['well_name'] = qpcr_well
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

    def is_populated(self):
        return all(v is not None for v in self.values())


def build_id_nested_plates(expt_plates: ExptPlates):

    id_plate_names = [p for p in expt_plates if p.endswith('_ID')]

    id_plates = {}
    for pn in id_plate_names:
        id_plates[pn] = []
        for w, reagents in expt_plates[pn].items():
            id_plates[pn].append(
                NestedIdConstituents.create(w, reagents, expt_plates))
    return id_plates


def group_nested_id_data(id_plate, instrument_data):

    nested_id_data = []
    id_grouped = group_by_id_assay(id_plate)
    for id_assay, id_nics in id_grouped.items():
        max_conc_mean_tm = \
            calc_max_conc_mean_tm(id_nics, instrument_data)
        pa_grouped = group_nested_by_pa_assay(id_nics)
        for pa_assay, pa_nics in pa_grouped.items():
            ntc_wells = get_ntc_wells(pa_nics)
            mean_ntc_ct = get_mean_ct(ntc_wells, instrument_data)
            for nic in pa_nics:
                nid = build_nested_id_data(nic, instrument_data,
                                           max_conc_mean_tm, mean_ntc_ct)
                if nid.is_populated():
                    nested_id_data.append(nid)
                else:
                    raise ValueError('Could not populate nested id data for '
                                     'well: {}'.format(nic['well_name']))

    return nested_id_data


def build_nested_id_data(nic, instrument_data, max_conc_mean_tm, mean_ntc_ct):
    well = nic['well_name']
    tms = get_tms(instrument_data[well])
    tm_delta = get_tm_delta(instrument_data[well], max_conc_mean_tm)

    ct = get_ct(instrument_data[well])
    delta_ct = get_delta_ct(ct, mean_ntc_ct)
    ct_call = get_ct_call(delta_ct)

    labels = get_product_labels_from_tms(tms, tm_delta,
                                         max_conc_mean_tm)
    spec = SPECIFIC_PRODUCT in labels
    non_spec = NON_SPECIFIC_PRODUCT in labels
    pd = PRIMER_DIMER in labels

    nid = NestedIdData.create_from_data(well, ct, delta_ct, ct_call, tms, spec,
                                        non_spec, pd)
    return nid


def calc_max_conc_mean_tm(nested_contents, inst_data):
    id_template_only_wells = get_id_template_only_wells(nested_contents)
    max_conc_wells = get_max_conc_template_wells(id_template_only_wells)
    max_conc_mean_tm = calc_mean_tm(max_conc_wells, inst_data)
    return max_conc_mean_tm


def group_by_id_assay(nested_contents):
    wells_by_id_assay = {}
    for nc in nested_contents:
        id_assay = nc.get_id_assay_attribute('reagent_name')
        wells_by_id_assay.setdefault(id_assay, []).append(nc)
    return wells_by_id_assay


def group_nested_by_pa_assay(nested_contents):
    wells_by_pa_assay = {}
    for nc in nested_contents:
        id_assay = nc.get_pa_assay_attribute('reagent_name')
        wells_by_pa_assay.setdefault(id_assay, []).append(nc)
    return wells_by_pa_assay


def get_id_template_only_wells(nested_contents: List[NestedIdConstituents]):
    id_template_only_wells = []
    for nc in nested_contents:
        if not nc.get_pa_template_attribute('reagent_name') and \
                nc.get_id_template_attribute('reagent_name'):
            id_template_only_wells.append(nc)
    return id_template_only_wells


def get_max_conc_template_wells(
        id_template_only_wells: List[NestedIdConstituents]):
    concs = [wc.get_id_template_attribute('concentration')
             for wc in id_template_only_wells]
    max_conc = max(concs)
    max_conc_wells = [wc for wc, c in zip(id_template_only_wells, concs)
                      if c == max_conc]
    return max_conc_wells
