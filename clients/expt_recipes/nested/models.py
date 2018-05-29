
"""
This module is responsible for the construction of nested assay screening
experiments.
"""


from typing import List, Dict
from collections import OrderedDict

from clients.expt_recipes.inst_data.data_models import IdQpcrData, LabChipData

from clients.expt_recipes.db_query import WellName, PlateName
from clients.expt_recipes.nested.constituents import IdConstituents


class NestedTableRow(OrderedDict):

    def __init__(self):
        super().__init__()

        self['qPCR Plate'] = None
        self['qPCR Well'] = None
        self['LC Plate'] = None
        self['LC Well'] = None
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
        self['∆NTC Ct'] = None
        self['Ct Call'] = None
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
    def create_from_models(cls, qpcr_well: WellName,
                           qpcr_plate: PlateName,
                           lc_well: WellName,
                           lc_plate: PlateName,
                           id_constit: IdConstituents,
                           id_qpcr_data: IdQpcrData,
                           lc_data: LabChipData):
        inst = cls()
        inst['qPCR Well'] = qpcr_well
        inst['qPCR Plate'] = qpcr_plate
        inst['LC Well'] = lc_well
        inst['LC Plate'] = lc_plate

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

    @classmethod
    def create_from_db(cls, qpcr_well: WellName,
                           qpcr_plate: PlateName,
                           lc_well: WellName,
                           lc_plate: PlateName,
                           id_constit: IdConstituents,
                           id_qpcr_data: IdQpcrData,
                           lc_data: LabChipData):
        inst = cls()
        inst['qPCR Well'] = qpcr_well
        inst['qPCR Plate'] = qpcr_plate
        inst['LC Well'] = lc_well
        inst['LC Plate'] = lc_plate

        inst['PA Assay Name'] = \
                _get_item_attribute('transferred_assays','reagent_name',id_constit)
        inst['PA Assay Conc.'] = \
            _get_item_attribute('transferred_assays', 'concentration',
                                id_constit)
        inst['PA Template Name'] = \
            _get_item_attribute('transferred_templates', 'reagent_name',
                                id_constit)
        inst['PA Template Conc.'] = \
            _get_item_attribute('transferred_templates', 'concentration',
                                id_constit)
        inst['PA Human Name'] = \
            _get_item_attribute('transferred_humans', 'reagent_name',
                                id_constit)
        inst['PA Human Conc.'] = \
            _get_item_attribute('transferred_humans', 'concentration',
                                id_constit)

        inst['ID Assay Name'] = \
            _get_item_attribute('assays', 'reagent_name',
                                id_constit)
        inst['ID Assay Conc.'] = \
            _get_item_attribute('assays', 'concentration',
                                id_constit)

        inst['ID Template Name'] = \
            _get_item_attribute('templates', 'reagent_name',
                                id_constit)
        inst['ID Template Conc.'] = \
            _get_item_attribute('templates', 'concentration',
                                id_constit)

        inst['ID Human Name'] = \
            _get_item_attribute('humans', 'reagent_name',
                                id_constit)
        inst['ID Human Conc.'] = \
            _get_item_attribute('humans', 'concentration',
                                id_constit)

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
            constits = id_constits[qw]
            id_qpcr_data = id_qpcr_datas[qw]
            lc_data = lc_datas[qw]
            r = NestedTableRow.create_from_models(qw, qpcr_plate, lw,
                                                  lc_plate, constits,
                                                  id_qpcr_data, lc_data)
            rows.append(r)

        inst = cls()
        inst.rows = rows
        return inst

    @classmethod
    def create_from_db(
            cls,
            qpcr_plate: str,
            lc_plate: str,
            mapping,
            id_constits: Dict[WellName, IdConstituents],
            id_qpcr_datas: IdQpcrData,
            lc_datas: LabChipData):

        rows = []
        for qw, lw in mapping.items():
            constits = id_constits[qw]
            id_qpcr_data = id_qpcr_datas[qw]
            lc_data = lc_datas[qw]
            r = NestedTableRow.create_from_db(qw, qpcr_plate, lw,
                                                  lc_plate, constits,
                                                  id_qpcr_data, lc_data)
            rows.append(r)

        inst = cls()
        inst.rows = rows
        return inst



def _get_item_attribute(key, attribute,contents):
    if key in contents:
        item = contents[key]
    else:
        item = []
    attributes = tuple(i[attribute] for i in item)
    return attributes