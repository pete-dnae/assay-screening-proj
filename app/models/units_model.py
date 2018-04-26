from django.db import models


class UnitsModel(models.Model):
    """
    Little more than a string.
    """
    abbrev = models.CharField(max_length=20, unique=True,primary_key=True)

    @classmethod
    def make(cls, abbrev):
        return UnitsModel.objects.create(abbrev = abbrev)
