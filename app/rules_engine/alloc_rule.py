from app.models.reagent_model import ReagentModel
from app.models.reagent_group_model import ReagentGroupModel

class AllocRule:
    """
    A allocation rule specifies a reagent (name), the cells to which it
    should be allocated on a plate and the concentration required.
    It uses a RowColIntersctions object to specify the cells.
    """

    def __init__(self, reagent_name, cells, conc, units):
        self.reagent_name = reagent_name
        self.cells = cells
        self.conc = conc
        self.units = units
        self.reagent_category = self._find_reagent_category()

    def _find_reagent_category(self):
        """
        Returns the reagent category from database
        Checks in reagent table first then in reagent group
        If it's a reagent group then the category of the first reagent in
        group is returned
        """
        category_found = ReagentModel.objects.filter(
            pk=self.reagent_name).first()
        if category_found:
            return category_found.category.name
        else:
            group_category = ReagentGroupModel.objects.filter(
            group_name=self.reagent_name).first()
        return group_category.reagent.category.name if \
            group_category else None