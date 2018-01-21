from django.db import models

from .primer_models import *


class Arg(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Strain(models.Model):
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
    strains = models.ManyToManyField(Strain)


