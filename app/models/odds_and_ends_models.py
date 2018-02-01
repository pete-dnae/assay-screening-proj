from copy import copy
from django.db import models

def mk_choices(items):
    """
    Utility to reduce typing when making 2-tuple lists required by
    model.choices.
    """
    return ((i,i) for i in items)

class CyclingPattern(models.Model):
    """
    A little lost model with no home to go to.
    """
    activation_time = models.PositiveIntegerField()
    activation_temp = models.PositiveIntegerField()
    num_cycles = models.PositiveIntegerField()
    denature_temp = models.PositiveIntegerField()
    denature_time = models.PositiveIntegerField()
    anneal_temp = models.PositiveIntegerField()
    anneal_time = models.PositiveIntegerField()
    extend_temp = models.PositiveIntegerField()
    extend_time = models.PositiveIntegerField()
