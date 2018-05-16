
from typing import List, Dict
import numpy as np

from clients.expt_recipes.common.models import IdQpcrData, LabChipData
from clients.expt_recipes.vanilla.constituents import IdConstituents

from collections import OrderedDict

from clients.expt_recipes.interp.db_query import WellName, PlateName


class VanillaTableRow(OrderedDict):

    def __init__(self):
        super().__init__()

        self['qPCR Plate'] = None
        self['qPCR Well'] = None
        self['LC Plate'] = None
        self['LC Well'] = None
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
        inst['qPCR Plate'] = qpcr_plate
        inst['qPCR Well'] = qpcr_well
        inst['LC Plate'] = lc_plate
        inst['LC Well'] = lc_well

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
            constits = id_constits[qw]
            id_qpcr_data = id_qpcr_datas[qw]
            lc_data = lc_datas[qw]
            r = VanillaTableRow.create_from_models(qw, qpcr_plate, lw,
                                                   lc_plate, constits,
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
    def create_from_table_rows(cls, rows):
        inst = cls()
        inst['qPCR Plate'] = cls._reduce('qPCR Plate', rows)
        inst['LC Plate'] = cls._reduce('LC Plate', rows)
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
        vals = [r[key] for r in rows if r[key] is not None]
        val = list(set(vals))
        if len(val) != 1:
            raise ValueError('{} does not return common value'.format(key))
        else:
            return val[0]

    @staticmethod
    def _count(key, rows):
        vals = [r[key] for r in rows if r[key] is not None]
        return vals.count(True)

    @staticmethod
    def _mean(key, rows):
        vals = [r[key] for r in rows if r[key] is not None]
        if all(np.isnan(vals)):
            return np.nan
        else:
            return np.nanmean(vals)

    @staticmethod
    def _min(key, rows):
        vals = [r[key] for r in rows if r[key] is not None]
        if all(np.isnan(vals)):
            return np.nan
        else:
            return np.nanmin(vals)

    @staticmethod
    def _max(key, rows):
        vals = [r[key] for r in rows if r[key] is not None]
        if all(np.isnan(vals)):
            return np.nan
        else:
            return np.nanmax(vals)


class VanillaSummaryTable:

    def __init__(self):
        self.rows = []

    @classmethod
    def create_from_summary_rows(cls, rows):
        inst = cls()
        inst.rows = rows
        return inst
