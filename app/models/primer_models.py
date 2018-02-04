"""
A group of closely related models - all concerned with Primers.
"""

from django.db import models

from .odds_and_ends_models import mk_choices
from .reagent_models import *


class Gene(models.Model):
    """
    Little more than a string - i.e. that name of the Gene. But formalized so
    it can take part in database relations.
    """
    name = models.CharField(primary_key=True, max_length=30, unique=True)


class Organism(models.Model):
    """
    For example "Eco", or it's longer proper name.
    """
    abbreviation = models.CharField(max_length=8, unique=True)
    full_name = models.CharField(max_length=30, unique=True)

    @classmethod
    def make(cls, abbr, full_name):
        return Organism.objects.create(abbreviation=abbr, full_name=full_name)


class Primer(models.Model):
    """
    Encapsulates on particular primer in terms of its foward or reverse role,
    its oligo code, and references to the Organism / Gene it targets.
    """

    primer_role_choices = mk_choices(('fwd', 'rev'))

    oligo_code = models.CharField(max_length=30)
    full_name = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=15, choices=primer_role_choices)
    organism = models.ForeignKey(Organism, 
        related_name='primer', on_delete=models.PROTECT)
    gene = models.ForeignKey(Gene, 
        related_name='primer', on_delete=models.PROTECT)


    @classmethod
    def make(self, organism, primer_name, fwd_or_rev, gene):
        return Primer.objects.create(
            oligo_code=organism,
            full_name=primer_name,
            role=fwd_or_rev,
            organism=organism,
            gene=gene
        )

class PrimerPair(models.Model):
    """
    Enapsulates two Primers that scientists have decided to use as a recognized
    pair, and whether for ID or preamp or both..

    Know know to be problematically oversimplified. These primer assemblies are
    not always simply pairs.
    """
    forward_primer = models.ForeignKey(Primer, 
        related_name='primer_pair_fwd', on_delete=models.PROTECT)
    reverse_primer = models.ForeignKey(Primer, 
        related_name='primer_pair_rev', on_delete=models.PROTECT)
    suitable_for_pa = models.BooleanField()
    suitable_for_id = models.BooleanField()

    class Meta:
        ordering = (
            'forward_primer__organism__abbreviation',
            'forward_primer__gene__name',
            'forward_primer__full_name',
            'reverse_primer__full_name'
        )


    @classmethod
    def make(cls, fwd_primer, rev_primer, for_pa, for_id):
        return PrimerPair.objects.create(
            forward_primer = fwd_primer,
            reverse_primer = rev_primer,
            suitable_for_pa = for_pa,
            suitable_for_id = for_id,
        )

    @classmethod
    def clone(cls, src):
        return PrimerPair.make(
            src.forward_primer, # Shared reuse
            src.reverse_primer, # Shared reuse
            src.suitable_for_pa, # Plain copy
            src.suitable_for_id # Plain copy
        )

    def display_name(self):
        """
        E.g. Efm_vanA_1.x_van05_van01
        """
        return '_'.join((
            self.forward_primer.organism.abbreviation,
            self.forward_primer.gene.name,
            self.forward_primer.full_name,
            self.reverse_primer.full_name,
            )
        )


class PrimerKit(models.Model):
    """
    Represents the primer pairs that a scientist has decided to pull together
    into a conceptual "kit" that will be used by one particular experiment.
    Every kit instance is dedicated to the experiment it belongs to. I.e. they
    are not shared. Carries also the concentration data that will be used for
    these at the meta level.
    """
    pa_primers = models.ManyToManyField(PrimerPair,
        related_name='primer_pair_pa')
    id_primers = models.ManyToManyField(PrimerPair,
        related_name='primer_pair_id')
    fwd_concentration = models.ForeignKey(Concentration, 
        related_name='primer_kit_fwd', on_delete=models.PROTECT)
    rev_concentration = models.ForeignKey(Concentration, 
        related_name='primer_kit_rev', on_delete=models.PROTECT)

    @classmethod
    def make(
        cls, pa_primers, id_primers, fwd_concentration, rev_concentration):
        primer_kit = PrimerKit.objects.create(
            fwd_concentration = fwd_concentration,
            rev_concentration = rev_concentration
        )
        for foo in pa_primers:
            primer_kit.pa_primers.add(foo)
        for p in id_primers:
            primer_kit.id_primers.add(p)
        primer_kit.save()
        return primer_kit

    @classmethod
    def clone(cls, src):
        return PrimerKit.make(
            [PrimerPair.clone(pp) for pp in src.pa_primers.all()], # New
            [PrimerPair.clone(pp) for pp in src.id_primers.all()], # New
            Concentration.clone(src.fwd_concentration), # New
            Concentration.clone(src.rev_concentration) # New
        )
