from django.db import models

from .reagent_category_model import ReagentCategoryModel


class ReagentModel(models.Model):
    """
    The reagent's name, plus the category it belongs to.
    """

    name = models.CharField(max_length=80, unique=True,primary_key=True)
    category = models.ForeignKey(
            ReagentCategoryModel, on_delete=models.PROTECT)
    opaque_payload = models.CharField(max_length=200,null=True)

    @classmethod
    def make(cls, name, category,opaque_payload=None):
        return ReagentModel.objects.create(
            name = name,
            category=category,
            opaque_payload = opaque_payload
        )
