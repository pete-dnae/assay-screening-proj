from django.db import models

from .odds_and_ends_models import mk_choices
from .reagent_models import *

class Gene(models.Model):
    name = models.CharField(primary_key=True, max_length=30, unique=True)

class Organism(models.Model):
    abbreviation = models.CharField(max_length=8, unique=True)
    full_name = models.CharField(max_length=30, unique=True)


class Primer(models.Model):

    primer_role_choices = mk_choices(('fwd', 'rev'))

    oligo_code = models.CharField(max_length=30)
    full_name = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=15, choices=primer_role_choices)
    organism = models.ForeignKey(Organism, 
        related_name='primer', on_delete=models.PROTECT)
    gene = models.ForeignKey(Gene, 
        related_name='primer', on_delete=models.PROTECT)


class PrimerPair(models.Model):
    forward_primer = models.ForeignKey(Primer, 
        related_name='primer_pair_fwd', on_delete=models.PROTECT)
    reverse_primer = models.ForeignKey(Primer, 
        related_name='primer_pair_rev', on_delete=models.PROTECT)
    suitable_for_pa = models.BooleanField()
    suitable_for_id = models.BooleanField()

    def display_name(self):
        """
        E.g. Efm_vanA_1.x_van05_van01
        """
        return '_'.join((
            self.forward_primer.organism.abbreviation,
            self.forward_primer.gene.name,
            self.forward_primer.oligo_code,
            self.reverse_primer.oligo_code,
            )
        )


class PrimerKit(models.Model):
    pa_primers = models.ManyToManyField(PrimerPair,
        related_name='primer_pair_pa')
    id_primers = models.ManyToManyField(PrimerPair,
        related_name='primer_pair_id')
    fwd_concentration = models.ForeignKey(Concentration, 
        related_name='primer_kit_fwd', on_delete=models.PROTECT)
    rev_concentration = models.ForeignKey(Concentration, 
        related_name='primer_kit_rev', on_delete=models.PROTECT)
