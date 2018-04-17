from collections import Counter
from functools import reduce
from collections import OrderedDict


class ImageRecipe:
    """
    Responsibility of this class is to decide what should go into images for one plate
    Does not get involved in making images , It's only responsibility is to specify what goes
    into images
    """

    def __init__(self, plate_info, reagent_category, exclusive_categories):

        self.plate_info = plate_info
        self.reagent_category = reagent_category
        self.common_entities = self.get_common_entities()
        self.exclusive_categories = exclusive_categories

    def prepare_image_spec(self):

        return self.get_filtered_entities()

    def get_common_entities(self):
        """
        Function returns a list of entities that are present in each well
        across a plate
        """

        entity_list = []

        for colno, entities in self.plate_info.items():

            for rowno, well_contents in entities.items():
                entity_list.append(well_contents)

        return reduce(lambda x, y: set(x).intersection(set(y)), entity_list)

    def entity_criteria_check(self, entity):
        """
        Function which decides whether a entity should be included or excluded
        """
        name, conc, unit = entity

        if name in self.reagent_category:
            if self.reagent_category[name] in self.exclusive_categories:
                return True
            elif entity not in self.common_entities:
                return True

    def get_filtered_entities(self):
        """
        Function which returns a dictionary keyed by cols
        and each cols key has a row dictionary and each
        row dictionary has a list of reagents that are to be shown

        Note : All the dictionaries are OrderedDict

        """

        table = OrderedDict()
        for col_no, entities in self.plate_info.items():
            row = table.setdefault(col_no, OrderedDict())
            for row_no, well_contents in entities.items():
                entities = row.setdefault(row_no, [])
                for entity in well_contents:
                    if self.entity_criteria_check(entity):
                        entities.append(entity)
        return table
