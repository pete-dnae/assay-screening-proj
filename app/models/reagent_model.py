from django.db import models

from .reagent_category_model import ReagentCategoryModel


class ReagentModel(models.Model):
    """
    The reagent's name, plus the category it belongs to.
    """
    name = models.CharField(max_length=80, unique=True) 
    category = models.ForeignKey(
            ReagentCategoryModel, on_delete=models.PROTECT)

    @classmethod
    def make(cls, name, category):
        return ReagentModel.objects.create(
            name = name,
            category=category
        )
