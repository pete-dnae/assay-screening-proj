from django.db import models
from .reagent_group_model import ReagentGroupModel
from .qpcr_results_model import QpcrResultsModel

class ReagentGroupWellLookupModel(models.Model):
    """
       This model does not provide anything that could not be worked out by
    cross examination of other tables.So why does it exist ? It exists as a
    convenient cache to support queries that cant afford the cost of cross
    examination.
       """

    well = models.ForeignKey(QpcrResultsModel,
                                      on_delete=models.PROTECT)
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
