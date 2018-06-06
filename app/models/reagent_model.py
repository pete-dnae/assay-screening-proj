from django.db import models
from django.contrib.postgres.fields import JSONField
from .reagent_category_model import ReagentCategoryModel


class ReagentModel(models.Model):
    """
    The reagent's name, plus the category it belongs to.
    """

    name = models.CharField(max_length=80, unique=True,primary_key=True)
    category = models.ForeignKey(
            ReagentCategoryModel, on_delete=models.PROTECT)
    # This field is to contain miscellaneous data as an opaque black box
    # which the reagent objects will take no interest in itself , its exists
    # solely for the benefit of downstream api clients
    opaque_json_payload = models.TextField(null=True)

    @classmethod
    def make(cls, name, category,opaque_json_payload=None):
        return ReagentModel.objects.create(
            name = name,
            category=category,
            opaque_json_payload = opaque_json_payload
        )
