
"""
This module is responsible for the construction of nested assay screening
experiments.
"""


from typing import List

from hardware.plates import ExptPlates

from collections import OrderedDict

from clients.reagents import ObjReagent
from clients.reagents import get_assays, get_templates, get_humans
from clients.transfers import get_transferred_assays, \
    get_transferred_templates, get_transferred_humans

from hardware.qpcr import qPCRInstWell
from hardware.labchip import LabChipInstWell, get_peaks
from clients.expt_recipes.well_constituents import WellConstituents
from clients.expt_recipes.results_interpretation.qpcr import calc_delta_ct,\
    get_ct_call, get_product_labels_from_tms
from hardware.qpcr import get_ct, get_tms, calc_tm_deltas
from clients.expt_recipes.results_interpretation.labchip import \
    get_product_label_from_labchip


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
        inst['templates'] = get_templates(reagents)
        inst['human'] = get_humans(reagents)
        inst['transferred_human'] = \
            get_transferred_humans(reagents, all_expt_plates)
        inst['transferred_templates'] =\
            get_transferred_templates(reagents, all_expt_plates)

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
    def create_from_inst_data(cls, qpcr_data: qPCRInstWell, max_conc_mean_tm,
                              mean_ntc_ct) -> 'NestedIdQpcrData':

        tms = get_tms(qpcr_data)
        tm_delta = calc_tm_deltas(qpcr_data, max_conc_mean_tm)
        ct = get_ct(qpcr_data)
        delta_ct = calc_delta_ct(ct, mean_ntc_ct)
        ct_call = get_ct_call(delta_ct)
        spec, non_spec, pd = get_product_labels_from_tms(tms, tm_delta,
                                                         max_conc_mean_tm)
        inst = cls()
        return inst.create(ct, delta_ct, ct_call, tms, spec, non_spec, pd)

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
        return inst

    @classmethod
    def create_from_inst_data(cls, labchip_well: LabChipInstWell,
                              expected_amp_lens, dilution):
        peaks = get_peaks(labchip_well)
        spec, non_spec, pd = \
            get_product_label_from_labchip(peaks, expected_amp_lens,
                                           dilution)
        inst = cls()
        return inst.create(spec, non_spec, pd)
