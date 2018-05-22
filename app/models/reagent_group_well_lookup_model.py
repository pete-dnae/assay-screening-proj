from django.db import models
from .reagent_group_model import ReagentGroupModel


class ReagentGroupWellLookupModel(models.Model):

    well = models.CharField(max_length=100)
    reagent_group = models.ForeignKey(ReagentGroupModel,
                                      on_delete=models.PROTECT)
    transfer = models.BooleanField()

    @classmethod
    def make(cls,well,reagent_group,transfer):
        ReagentGroupWellLookupModel.objects.create(
            well=well,
            reagent_group=reagent_group,
            transfer=transfer
        )
