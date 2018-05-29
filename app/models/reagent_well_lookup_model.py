from django.db import models
from .reagent_model import ReagentModel


class ReagentWellLookupModel(models.Model):
    """
    This model does not provide anything that could not be worked out by
    cross examination of other tables.So why does it exist ? It exists as a
    convenient cache to support queries that cant afford the cost of cross
    examination.
    """
    well = models.CharField(max_length=100)
    reagent = models.ForeignKey(ReagentModel,on_delete=models.PROTECT)
    transfer = models.BooleanField()

    @classmethod
    def make(cls,well,reagent,transfer):
        return ReagentWellLookupModel.objects.create(
            well=well,
            reagent=reagent,
            transfer=transfer
        )