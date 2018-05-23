from django.db import models
from .reagent_model import ReagentModel


class ReagentWellLookupModel(models.Model):
    """
    Model is created to provide ease of access to a qpcr well result
    This model captures relationship between a qpcr well and the reagents
    allocated in the well during experiment design
    It has additional transfer flag to indicate reagents transferred to a
    qpcr well
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