
from typing import List, Dict
import numpy as np

from clients.expt_recipes.common.models import IdQpcrData, LabChipData, \
    WellConstituents
from hardware.plates import ExptPlates, WellName, PlateName

from collections import OrderedDict

from clients.reagents import ObjReagent, get_assays, get_templates, get_humans


class IdConstituents(WellConstituents):

    def __init__(self):
        super().__init__()

    @classmethod
    def create(cls, reagents: List[ObjReagent],
               all_expt_plates: ExptPlates) -> 'IdConstituents':

        inst = cls()
        inst['assays'] = get_assays(reagents)
        inst['templates'] = get_templates(reagents)
        inst['human'] = get_humans(reagents)

        return inst

    def get_id_assay_attribute(self, attribute):
        return self._get_item_attribute('assays', attribute)

    def get_id_template_attribute(self, attribute):
        return self._get_item_attribute('templates', attribute)

    def get_id_human_attribute(self, attribute):
        return self._get_item_attribute('human', attribute)


class VanillaTableRow(OrderedDict):

    def __init__(self):
        super().__init__()

        self['qPCR well'] = None
        self['LC well'] = None
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
    def create_from_models(cls, qpcr_well: WellName, lc_well: WellName,
                           id_constit: IdConstituents,
                           id_qpcr_data: IdQpcrData,
                           lc_data: LabChipData):
        inst = cls()
        inst['qPCR well'] = qpcr_well
        inst['LC well'] = lc_well

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


class VanillaMasterTable:

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
            r = VanillaTableRow.create_from_models(qwell, lcwell, constits,
                                                   id_qpcr_data, lc_data)
            rows.append(r)

        inst = cls()
        inst.rows = rows
        return inst


class VanillaSummaryRow(OrderedDict):

    def __init__(self):
        super().__init__()

        self['qPCR Plate'] = None
        self['LC Plate'] = None
        self['ID Assay Name'] = None
        self['ID Assay Conc.'] = None
        self['ID Template Name'] = None
        self['ID Template Conc.'] = None
        self['ID Human Name'] = None
        self['ID Human Conc.'] = None
        self['Reps'] = None
        self['#Ct Pos'] = None
        self['#Tm Specif'] = None
        self['#Tm NS'] = None
        self['#Tm PD'] = None
        self['Min Ct'] = None
        self['Mean Ct'] = None
        self['Max Ct'] = None
        self['Mean ∆NTC Ct'] = None
        self['Min Tm1'] = None
        self['Mean Tm1'] = None
        self['Max Tm1'] = None
        self['Mean Specif ng/ul'] = None
        self['Mean NS ng/ul'] = None
        self['Mean PD ng/ul'] = None

    @classmethod
    def create_from_table_rows(cls, qpcr_plate: PlateName,
                               lc_plate: PlateName,
                               rows):
        inst = cls()
        inst['qPCR Plate'] = qpcr_plate
        inst['LC Plate'] = lc_plate
        inst['ID Assay Name'] = cls._reduce('ID Assay Name', rows)
        inst['ID Assay Conc.'] = cls._reduce('ID Assay Conc.', rows)
        inst['ID Template Name'] = cls._reduce('ID Template Name', rows)
        inst['ID Template Conc.'] = cls._reduce('ID Template Conc.', rows)
        inst['ID Human Name'] = cls._reduce('ID Human Name', rows)
        inst['ID Human Conc.'] = cls._reduce('ID Human Conc.', rows)
        inst['Reps'] = len(rows)
        inst['#Ct Pos'] = cls._count('Ct Call', rows)
        inst['#Tm Specif'] = cls._count('Tm Specif', rows)
        inst['#Tm NS'] = cls._count('Tm NS', rows)
        inst['#Tm PD'] = cls._count('Tm PD', rows)
        inst['Min Ct'] = cls._min('Ct', rows)
        inst['Mean Ct'] = cls._mean('Ct', rows)
        inst['Max Ct'] = cls._max('Ct', rows)
        inst['Mean ∆NTC Ct'] = cls._mean('∆NTC Ct', rows)
        inst['Min Tm1'] = cls._min('Tm1', rows)
        inst['Mean Tm1'] = cls._mean('Tm1', rows)
        inst['Max Tm1'] = cls._max('Tm1', rows)
        inst['Mean Specif ng/ul'] = cls._mean('Specif ng/ul', rows)
        inst['Mean NS ng/ul'] = cls._mean('NS ng/ul', rows)
        inst['Mean PD ng/ul'] = cls._mean('PD ng/ul', rows)

        return inst

    @staticmethod
    def _reduce(key, rows):
        val = list(set([r[key] for r in rows]))
        if len(val) != 1:
            raise ValueError('{} does not return common value'.format(key))
        else:
            return val[0]

    @staticmethod
    def _count(key, rows):
        return len([r[key] for r in rows if r])

    @staticmethod
    def _mean(key, rows):
        return np.nanmean([r[key] for r in rows])

    @staticmethod
    def _min(key, rows):
        return np.nanmin([r[key] for r in rows])

    @staticmethod
    def _max(key, rows):
        return np.nanmax([r[key] for r in rows])

class VanillaSummaryTable:

    def __init__(self):
        self.rows = []
