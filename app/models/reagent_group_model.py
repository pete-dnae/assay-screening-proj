from django.db import models

from .reagent_model import ReagentModel
from .reagent_category_model import ReagentCategoryModel


class ReagentGroupModel(models.Model):
    """
    A thing that specifies a group of ReagentModel(s)..
    """
    name = models.CharField(max_length=40, unique=True) 
    category = models.ForeignKey(
            ReagentCategoryModel, on_delete=models.PROTECT)
    members = models.ManyToManyField(ReagentModel)

    @classmethod
    def make(cls, name, category, members):
        instance =  ReagentGroupModel.objects.create(
            name = name,
            category = category,
        )
        instance.members.add(*members)
        return instance
