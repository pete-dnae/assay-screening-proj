from django.db import models
from .reagent_group_model import ReagentGroupModel


class ReagentGroupWellLookupModel(models.Model):
    """
       Model is created to provide ease of access to a qpcr well result
       This model captures relationship between a qpcr well and the reatgent
       GROUPS allocated in the well during experiment design
       It has additional transfer flag to indicate reagentgroups transferred
       to a qpcr well
       """

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
