
"""
This module is responsible for the construction of nested assay screening
experiments.
"""


from typing import List, Dict

from hardware.plates import ExptPlates, WellName

from collections import OrderedDict

from clients.reagents import ObjReagent, get_assays, get_templates, get_humans
from clients.transfers import get_transferred_assays, \
    get_transferred_templates, get_transferred_humans

from clients.expt_recipes.well_constituents import WellConstituents
import clients.expt_recipes.interp.qpcr as intq
import clients.expt_recipes.interp.labchip as intlc
import hardware.qpcr as hwq
import hardware.labchip as hwlc


class IdQpcrConstituents(WellConstituents):

    def __init__(self):
        super().__init__()
        self['transferred_assays'] = None
        self['transferred_templates'] = None
        self['transferred_human'] = None

    @classmethod
    def create(cls, reagents: List[ObjReagent],
               all_expt_plates: ExptPlates) -> 'IdQpcrConstituents':

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


class NestedTableRow(OrderedDict):

    def __init__(self):
        super().__init__()

        self['qPCR well'] = None
        self['LC well'] = None
        self['PA Assay Name'] = None
        self['PA Assay Conc.'] = None
        self['PA template Name'] = None
        self['PA Template Conc.'] = None
        self['PA Human Name'] = None
        self['PA Human Conc.'] = None
        self['ID Assay Name'] = None
        self['ID Assay Conc.'] = None
        self['ID Template Name'] = None
        self['ID Template Conc.'] = None
        self['ID Human Name'] = None
        self['ID Human Conc.'] = None
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
        self['Specif ng/ul'] = None
        self['NS ng/ul'] = None
        self['PD ng/ul'] = None

    @classmethod
    def create_from_models(cls, qpcr_well: WellName, lc_well: WellName,
                           id_constit: IdQpcrConstituents,
                           id_qpcr_data: IdQpcrData,
                           lc_data: LabChipData):
        inst = cls()
        inst['qPCR well'] = qpcr_well
        inst['LC well'] = lc_well

        inst['PA Assay Name'] = \
            id_constit.get_pa_assay_attribute('reagent_name')
        inst['PA Assay Conc.'] = \
            id_constit.get_pa_assay_attribute('concentration')

        inst['PA Template Name'] = \
            id_constit.get_pa_template_attribute('reagent_name')
        inst['PA Template Conc.'] = \
            id_constit.get_pa_template_attribute('concentration')

        inst['PA Human Name'] = \
            id_constit.get_pa_human_attribute('reagent_name')
        inst['PA Human Conc.'] = \
            id_constit.get_pa_human_attribute('concentration')

        inst['ID Assay Name'] = \
            id_constit.get_id_assay_attribute('reagent_name')
        inst['ID Assay Conc.'] = \
            id_constit.get_id_assay_attribute('concentration')

        inst['ID Template Name'] = \
            id_constit.get_id_template_attribute('reagent_name')
        inst['ID Template Conc.'] = \
            id_constit.get_id_template_attribute('concentration')

        inst['ID Human Name'] = \
            id_constit.get_id_human_attribute('reagent_name')
        inst['ID Human Conc.'] = \
            id_constit.get_id_human_attribute('concentration')

        for k, v in id_qpcr_data.items():
            inst[k] = v

        for k, v in lc_data.items():
            inst[k] = v

        return inst


class NestedMasterTable:

    def __init__(self):

        self.rows = []

    @classmethod
    def create_from_models(
            cls,
            qpcr_wells: List[WellName],
            qpcr_plate: str,
            lc_wells: List[WellName],
            lc_plate: str,
            id_constits: Dict[WellName, IdQpcrConstituents],
            id_qpcr_datas: IdQpcrData,
            lc_datas: LabChipData):

        rows = []
        for qw, lw in zip(qpcr_wells, lc_wells):
            qwell = '{}_{}'.format(qpcr_plate, qw)
            lcwell = '{}_{}'.format(lc_plate, lw)
            constits = id_constits[qw]
            id_qpcr_data = id_qpcr_datas[qw]
            lc_data = lc_datas[qw]
            r = NestedTableRow.create_from_models(qwell, lcwell, constits,
                                                  id_qpcr_data, lc_data)
            rows.append(r)

        inst = cls()
        inst.rows = rows
        return inst
