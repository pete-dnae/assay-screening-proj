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
