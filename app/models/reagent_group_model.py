from django.db import models

from .reagent_model import ReagentModel
from .reagent_category_model import ReagentCategoryModel
from .units_model import UnitsModel


class ReagentGroupModel(models.Model):
    """
    Contains all the reagent group names defined
    """
    group_name = models.CharField(max_length=40,primary_key=True)


    @classmethod
    def make(cls, group_name):
        return ReagentGroupModel.objects.create(group_name = group_name)


class ReagentGroupDetailsModel(models.Model):
    """
    Captures one to many relationship between a reagent group and its
    constituents
    Contains details about reagent  used in a reagent group ,has pointers to
    reagent group and reagents
    """
    reagent_group = models.ForeignKey(ReagentGroupModel,
                                      related_name='details',
                                      on_delete=models.CASCADE)
    reagent = models.ForeignKey(ReagentModel, on_delete=models.PROTECT)
    concentration = models.FloatField()
    units = models.ForeignKey(UnitsModel, on_delete=models.PROTECT)

    @classmethod
    def make(cls, reagent_group, reagent, concentration, units):
        return ReagentGroupDetailsModel.objects.create(
            reagent_group=reagent_group,
            reagent=reagent,
            concentration=concentration,
            units=units,
        )