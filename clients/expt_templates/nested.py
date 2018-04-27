
from typing import List

from clients.expt_templates.well_contents import WellContents
from clients.reagents import Reagent
from hardware.plates import Plates
from collections import OrderedDict

from clients.reagents import get_assays, get_templates, disambiguate_templates
from clients.transfers import get_transferred_assays, get_transferred_templates


class NestedWellContents(WellContents):

    def __init__(self):
        super().__init__()

    @classmethod
    def create(cls, qpcr_well_id: str, reagents: List[Reagent],
               plates: Plates) -> 'NestedWellContents':

        inst = cls()
        inst['well_name'] = qpcr_well_id
        inst['assays'] = get_assays(reagents)
        inst['transferred_assays'] = get_transferred_assays(reagents, plates)
        inst['human'], inst['templates'] = \
            disambiguate_templates(get_templates(reagents))
        inst['transferred_human'], inst['transferred_templates'] = \
            disambiguate_templates(get_transferred_templates(reagents, plates))

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


class NestedQPCRData(OrderedDict):

    def __init__(self):
        super().__init__()
        self['qPCR Well'] = None
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
    def create_from_data(cls, qpcr_well, qpcr_data) -> 'NestedQPCRData':
        inst = cls()
        inst['qPCR Well'] = qpcr_well
        # inst['Ct'] = get_ct(qpcr_data)
        inst['∆NTC_Ct'] = None
        inst['Ct_Call'] = None
        # inst['Tm1'] = _get_tm(qpcr_data, 'tm1')
        # inst['Tm2'] = _get_tm(qpcr_data, 'tm2')
        # inst['Tm3'] = _get_tm(qpcr_data, 'tm3')
        # inst['Tm4'] = _get_tm(qpcr_data, 'tm4')
        inst['Tm Specif'] = None
        inst['Tm NS'] = None
        inst['Tm PD'] = None

        return inst

    def is_populated(self):
        return all(v is not None for v in self.values())


def build_nested(plates: Plates):

    pa_plates = [p for p in plates if p.endswith('PA')]
    id_plates = [p for p in plates if p.endswith('ID')]
    lc_plates = [p for p in plates if p.startswith('LC')]

    nested_summaries = {}

    for p in id_plates:
        for w, reagents in plates[p].items():
            ns = NestedWellContents.create(w, reagents, plates)
            nested_summaries[w] = ns

    return nested_summaries
