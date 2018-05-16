import abc
from collections import OrderedDict

from clients.expt_recipes.interp.qpcr import calc_delta_ct, get_ct_call, \
    get_product_labels_from_tms
from clients.expt_recipes.interp.labchip import \
    get_product_label_from_peak_bp_concs
from hardware.qpcr import get_tms, calc_tm_deltas, get_ct
from hardware.labchip import extract_bp_conc_pairs


class WellConstituents(OrderedDict):

    def __init__(self):
        super().__init__()
        self['assays'] = None
        self['templates'] = None
        self['human'] = None

    @classmethod
    @abc.abstractmethod
    def create(cls, *args, **kwargs):
        inst = cls()
        return inst

    def _get_item_attribute(self, key, attribute):
        item = self[key]
        attributes = tuple(i[attribute] for i in item)
        return attributes

    def get_id_assay_attribute(self, attribute):
        return self._get_item_attribute('assays', attribute)

    def get_id_template_attribute(self, attribute):
        return self._get_item_attribute('templates', attribute)

    def get_id_human_attribute(self, attribute):
        return self._get_item_attribute('human', attribute)

    def is_populated(self):
        return all(v is not None for v in self.values())


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

        tms = get_tms(qinst_data)
        tm_delta = calc_tm_deltas(qinst_data, max_conc_mean_tm)
        ct = get_ct(qinst_data)
        delta_ct = calc_delta_ct(ct, mean_ntc_ct)
        ct_call = get_ct_call(delta_ct)
        spec, non_spec, pd = get_product_labels_from_tms(tms, tm_delta,
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
    def create_from_inst_data(cls, linst_data, expected_amp_lens, dilution):
        bp_concs = extract_bp_conc_pairs(linst_data)
        spec, non_spec, pd = \
            get_product_label_from_peak_bp_concs(bp_concs,
                                                 expected_amp_lens,
                                                 dilution)
        inst = cls()
        return inst.create(spec, non_spec, pd)
