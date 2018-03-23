from django.db import models


class ReagentCategoryModel(models.Model):
    """
    A reagent must belong to a category (like Primer or hDNA). This table
    defines what categories are available.
    """
    name = models.CharField(max_length=40, unique=True) 

    @classmethod
    def make(cls, name):
        return ReagentCategoryModel.objects.create(name = name)
