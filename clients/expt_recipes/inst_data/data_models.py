from collections import OrderedDict

from clients.expt_recipes.inst_data import qpcr
from clients.expt_recipes.inst_data import labchip


class IdQpcrData(OrderedDict):

    def __init__(self):
        super().__init__()
        self['Ct'] = None
        self['∆NTC Ct'] = None
        self['Ct Call'] = None
        self['Tm1'] = None
        self['Tm2'] = None
        self['Tm3'] = None
        self['Tm4'] = None
        self['Tm Specif'] = None
        self['Tm NS'] = None
        self['Tm PD'] = None

    @classmethod
    def create(cls, ct, delta_ct, ct_call, tms, spec, non_spec, pd):
        inst = cls()
        inst['Ct'] = ct
        inst['∆NTC Ct'] = delta_ct
        inst['Ct Call'] = ct_call
        inst['Tm1'] = tms[0]
        inst['Tm2'] = tms[1]
        inst['Tm3'] = tms[2]
        inst['Tm4'] = tms[3]
        inst['Tm Specif'] = spec
        inst['Tm NS'] = non_spec
        inst['Tm PD'] = pd
        return inst

    @classmethod
    def create_from_inst_data(cls, qinst_data, max_conc_mean_tm, mean_ntc_ct):
        payload = qpcr.create_payload(qinst_data, max_conc_mean_tm, mean_ntc_ct)
        inst = cls()
        return inst.create(*payload)


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
    def create_from_inst_data(cls, linst_data, expected_amp_lens, dilution):
        payload = labchip.create_payload(linst_data, expected_amp_lens,
                                         dilution)
        inst = cls()
        return inst.create(*payload)
