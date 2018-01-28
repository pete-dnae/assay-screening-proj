"""
A few closely related models that concern Strains.
"""

from django.db import models

from .primer_models import *


class Arg(models.Model):
    """
    An antibiotic resistant Gene.
    """
    name = models.CharField(max_length=30, unique=True)


class Strain(models.Model):
    """
    A bacteria strain in terms of the organism of which it is a specialism
    of, optionally the ARG it contains and its genome length.
    """
    name = models.CharField(max_length=30, unique=True)
    organism = models.ForeignKey(Organism, 
        related_name='strain_organism', on_delete=models.PROTECT)
    arg = models.ForeignKey(Arg, 
        related_name='strain_arg', null=True, on_delete=models.PROTECT)
    genome_size = models.BigIntegerField()

    class Meta:
        ordering = ('organism__abbreviation', 'arg__name')

    def display_name(self):
        buf = self.organism.abbreviation
        if self.arg:
            buf = '_'.join((buf, self.arg.name))
        return buf


class StrainKit(models.Model):
    """
    The set of Strains that a scientest has decided to assemble as the
    conceptual kit to deploy in an experiment.
    """
    strains = models.ManyToManyField(Strain)


