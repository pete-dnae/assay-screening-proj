from django.db import models
from .reagent_model import ReagentModel


class ReagentWellLookupModel(models.Model):

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