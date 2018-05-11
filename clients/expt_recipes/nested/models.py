
"""
This module is responsible for the construction of nested assay screening
experiments.
"""


from typing import List, Dict
from collections import OrderedDict

from clients.expt_recipes.common.models import IdQpcrData, LabChipData, \
    WellConstituents
from hardware.plates import ExptPlates, WellName

from clients.reagents import ObjReagent, get_assays, get_templates, get_humans
from clients.transfers import get_transferred_assays, \
    get_transferred_templates, get_transferred_humans


class IdConstituents(WellConstituents):

    def __init__(self):
        super().__init__()
        self['transferred_assays'] = None
        self['transferred_templates'] = None
        self['transferred_human'] = None

    @classmethod
    def create(cls, reagents: List[ObjReagent],
               all_expt_plates: ExptPlates) -> 'IdConstituents':

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

    def get_pa_assay_attribute(self, attribute):
        return self._get_item_attribute('transferred_assays', attribute)

    def get_pa_template_attribute(self, attribute):
        return self._get_item_attribute('transferred_templates', attribute)

    def get_pa_human_attribute(self, attribute):
        return self._get_item_attribute('transferred_human', attribute)


class NestedTableRow(OrderedDict):

    def __init__(self):
        super().__init__()

        self['qPCR well'] = None
        self['LC well'] = None
        self['PA Assay Name'] = None
        self['PA Assay Conc.'] = None
        self['PA Template Name'] = None
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
                           id_constit: IdConstituents,
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
            id_constits: Dict[WellName, IdConstituents],
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
