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

    @classmethod
    def make( cls, activation_time, activation_temp, num_cycles, 
            denature_temp, denature_time, anneal_temp, anneal_time, 
            extend_temp, extend_time):
        return CyclingPattern.objects.create(
            activation_time = activation_time,
            activation_temp = activation_temp,
            num_cycles = num_cycles,
            denature_temp = denature_temp,
            denature_time = denature_time,
            anneal_temp = anneal_temp,
            anneal_time = anneal_time,
            extend_temp = extend_temp,
            extend_time = extend_time
        )

    @classmethod
    def clone(cls, src):
        return cls.make(
            src.activation_time, # All plain copies
            src.activation_temp,
            src.num_cycles,
            src.denature_temp,
            src.denature_time,
            src.anneal_temp,
            src.anneal_time,
            src.extend_temp,
            src.extend_time
        )
