from django.db import models


class ReagentNameModel(models.Model):
    """
    Little more than a string.
    """
    name = models.CharField(max_length=80, unique=True) 

    @classmethod
    def make(cls, name):
        return ReagentNameModel.objects.create(name = name)
