
from collections import OrderedDict
from clients.expt_recipes.db_query import get_assays, \
    get_transferred_assays, get_templates, get_humans, \
    get_transferred_humans, get_transferred_templates


class IdConstituents(OrderedDict):

    def __init__(self):
        super().__init__()
        self['transferred_assays'] = None
        self['transferred_templates'] = None
        self['transferred_human'] = None

    @classmethod
    def create(cls, reagents, all_expt_plates):

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

    def _get_item_attribute(self, key, attribute):
        item = self[key]
        attributes = tuple(i[attribute] for i in item)
        return attributes

    def get_pa_assay_attribute(self, attribute):
        return self._get_item_attribute('transferred_assays', attribute)

    def get_pa_template_attribute(self, attribute):
        return self._get_item_attribute('transferred_templates', attribute)

    def get_pa_human_attribute(self, attribute):
        return self._get_item_attribute('transferred_human', attribute)

    def get_id_assay_attribute(self, attribute):
        return self._get_item_attribute('assays', attribute)

    def get_id_template_attribute(self, attribute):
        return self._get_item_attribute('templates', attribute)

    def get_id_human_attribute(self, attribute):
        return self._get_item_attribute('human', attribute)
