from functools import reduce
from collections import OrderedDict


class ImageRecipe:
    """
    Responsibility of this class is to decide what should go into images for
    one plate. Does not get involved in making images , It's only
    responsibility is to decide what images are required for a plate and what
    should go into them.

    Usage Instructions:
        Create a ImageRecipe object with allocation info for a plate and 
        reagents categories
    """


    def __init__(self, plate_info):
        """
         Provide a dictionary keyed on column number ,with values that are
         dictionaries keyed on row number and well contents as values.

        """

        self.plate_info = plate_info
        self.common_reagents = self._get_common_reagents()

    def make_image_spec(self):
        """
        Function must be called after initializing the class to get a
        dictionary with same structure as plate_info but with reagents that
        are eligible to be on display.
        """
        return self._get_filtered_reagents()

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _get_common_reagents(self):
        """
        Function returns a list of reagents that are present in each well
        across a plate
        """

        entity_list = []

        for colno, reagents in self.plate_info.items():

            for rowno, well_contents in reagents.items():
                entity_list.append(well_contents)

        return reduce(lambda x, y: set(x).intersection(set(y)), entity_list)

    def _reagent_criteria_check(self, reagent):
        """
        Function which decides whether a entity should be included or excluded
        """
        name, conc, unit,category = reagent
        
        if reagent not in self.common_reagents:
            return True
        return False

    def _get_filtered_reagents(self):
        """
        Function which returns a dictionary keyed by cols
        and each cols key has a row dictionary and each
        row dictionary has a list of reagents that are to be shown

        Note : All the dictionaries are OrderedDict

        """

        table = OrderedDict()
        for col_no, reagents in self.plate_info.items():
            row = table.setdefault(col_no, OrderedDict())
            for row_no, well_contents in reagents.items():
                reagents = row.setdefault(row_no, [])
                for reagent in well_contents:
                    if self._reagent_criteria_check(reagent):
                        reagents.append(reagent)
        return table