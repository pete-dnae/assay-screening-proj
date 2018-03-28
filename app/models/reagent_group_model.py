from django.db import models

from .reagent_model import ReagentModel
from .reagent_category_model import ReagentCategoryModel
from .units_model import UnitsModel


class ReagentGroupModel(models.Model):
    """
    Defines rows in a table that makes it possible to use sets of its rows to
    define named groups of existing reagents, along with the concentrations at
    which they are present.
    """
    group_name = models.CharField(max_length=40, unique=False) 
    reagent = models.ForeignKey(ReagentModel, on_delete=models.PROTECT)
    concentration = models.FloatField()
    units = models.ForeignKey(UnitsModel, on_delete=models.PROTECT)

    @classmethod
    def make(cls, group_name, reagent, concentration, units):
        return  ReagentGroupModel.objects.create(
            group_name = group_name,
            reagent = reagent,
            concentration = concentration,
            units = units,
        )
