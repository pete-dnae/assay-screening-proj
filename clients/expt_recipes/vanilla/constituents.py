
from collections import OrderedDict

from clients.expt_recipes.interp.db_query import get_assays, get_templates, \
    get_humans


class IdConstituents(OrderedDict):

    def __init__(self):
        super().__init__()

    @classmethod
    def create(cls, reagents):

        inst = cls()
        inst['assays'] = get_assays(reagents)
        inst['templates'] = get_templates(reagents)
        inst['human'] = get_humans(reagents)

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
