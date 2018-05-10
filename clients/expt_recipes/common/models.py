from collections import OrderedDict
from typing import Dict

from clients.expt_recipes.interp import qpcr as intq, labchip as intlc
from hardware import qpcr as hwq, labchip as hwlc
from hardware.plates import WellName


class IdQpcrData(OrderedDict):

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
            'IdQpcrData':
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
    def create_from_inst_data(cls, qpcr_data: hwq.qPCRInstWell,
                              max_conc_mean_tm,
                              mean_ntc_ct) -> 'IdQpcrData':

        tms = hwq.get_tms(qpcr_data)
        tm_delta = hwq.calc_tm_deltas(qpcr_data, max_conc_mean_tm)
        ct = hwq.get_ct(qpcr_data)
        delta_ct = intq.calc_delta_ct(ct, mean_ntc_ct)
        ct_call = intq.get_ct_call(delta_ct)
        spec, non_spec, pd = intq.get_product_labels_from_tms(tms, tm_delta,
                                                              max_conc_mean_tm)
        inst = cls()
        return inst.create(ct, delta_ct, ct_call, tms, spec, non_spec, pd)

    def is_populated(self):
        return all(v is not None for v in self.values())


class LabChipData(OrderedDict):

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
    def create_from_inst_data(cls, labchip_well: hwlc.LabChipInstWell,
                              expected_amp_lens, dilution):
        peaks = hwlc.get_peaks(labchip_well)
        spec, non_spec, pd = \
            intlc.get_product_label_from_labchip(peaks, expected_amp_lens,
                                                 dilution)
        inst = cls()
        return inst.create(spec, non_spec, pd)


LabChipDatas = Dict[WellName, LabChipData]
qPCRDatas = Dict[WellName, IdQpcrData]