
from collections import OrderedDict
import abc


class WellConstituents(OrderedDict):

    def __init__(self):
        super().__init__()
        self['assays'] = None
        self['transferred_assays'] = None
        self['templates'] = None
        self['transferred_templates'] = None
        self['human'] = None
        self['transferred_human'] = None

    @classmethod
    @abc.abstractmethod
    def create(cls, *args, **kwargs):
        inst = cls()
        return inst

    def _get_item_attribute(self, key, attribute):
        item = self[key]
        attributes = tuple(i[attribute] for i in item)
        return attributes

    def is_populated(self):
        return all(v is not None for v in self.values())
