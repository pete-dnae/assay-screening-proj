"""
A set of related model classes that help us define reagents.

This model is know to be quite badly flawed and represent really just a line in
the sand from which to get going.

In particular we must define the conceptual entities more rigourously.
And explore the abandoment of all references to volumes in favour of
concentrations.
"""

from django.db import models

from .odds_and_ends_models import mk_choices


class Concentration(models.Model):
    """
    A utility class to encapsulate one particular concentraction value
    """

    units_choices = mk_choices((
        'X',
        'mM',
        'mg/ml',
        'mM each',
        'microM each',
        'ng/ul',
        'cp/ul',
        '%'))

    stock = models.DecimalField(max_digits=8, decimal_places=2)
    final = models.DecimalField(max_digits=8, decimal_places=2)
    units = models.CharField(max_length=15, choices=units_choices)

    @classmethod
    def make(cls, stock, final, units):
        return Concentration.objects.create(
            stock=stock, final=final, units=units)


class ConcreteReagent(models.Model):
    """
    One of several types of reagent we acknowledge in the system. In this case
    one that is bought-in and is physically sitting in some bottle somewhere.
    Hence it has its own concentration.
    """
    name = models.CharField(max_length=30) # Names are not unique!
    lot = models.CharField(max_length=30)
    concentration = models.ForeignKey(
        Concentration, related_name='reagent', on_delete=models.PROTECT)

    @classmethod
    def make(self, name, lot, stock, final, units):
        concentration = Concentration.make(stock, final, units)
        reagent = ConcreteReagent.objects.create(
            name=name, lot=lot, concentration=concentration)
        return reagent


class BufferMix(models.Model):
    """
    We model two types of mixture explicitly, of which this is one.
    This one captures a list of ConcreteReagents that will be mixed to be used
    downstream..
    """
    concrete_reagents = models.ManyToManyField(ConcreteReagent)
    volume = models.PositiveIntegerField()
    final_volume = models.PositiveIntegerField()


class MixedReagent(models.Model):
    """
    A wrapper around a BufferMix, which allows the same BufferMix to be used at
    alternative concentrations.
    """
    MIXED_REAGENT = 'mixed_reagent'
    buffer_mix = models.ForeignKey(BufferMix, 
        related_name=MIXED_REAGENT, on_delete=models.PROTECT)
    concentration = models.ForeignKey(Concentration, 
        related_name=MIXED_REAGENT, on_delete=models.PROTECT)


class PlaceholderReagent(models.Model):
    """
    A type of virtual reagent we recognize that can be talked about in in 
    vague terms in parts of our model, but for which the details are specified
    elsehwere.
    """
    type_choices = mk_choices(('Primers', 'Template', 'HgDNA'))

    type = models.CharField(max_length=15, choices=type_choices)
    concentration = models.ForeignKey(Concentration, 
        related_name='placeholder_reagent', on_delete=models.PROTECT)

    @classmethod
    def make(self, placeholder_type, stock, final, units):
        return PlaceholderReagent.objects.create(
            type=placeholder_type,
            concentration=Concentration.make(stock, final, units)
        )


class MasterMix(models.Model):
    """
    Our second kind of recognized mixture. In this case teh MasterMix is
    comprised, by definition of a water component, a reference to a buffer mix,
    and references to PlacehoderReagents such as 'Primers' or 'HgDNA'.
    """
    water = models.ForeignKey(ConcreteReagent, 
        related_name='master_mix_water', on_delete=models.PROTECT)
    buffer_mix = models.ForeignKey(MixedReagent,
        related_name='master_mix_buffermix', on_delete=models.PROTECT)
    primers = models.ForeignKey(PlaceholderReagent,
        related_name='master_mix_primers', on_delete=models.PROTECT)
    hgDNA = models.ForeignKey(PlaceholderReagent,
        related_name='master_mix_hgDNA', null=True, on_delete=models.PROTECT)
    template = models.ForeignKey(PlaceholderReagent,
        related_name='master_mix_template', on_delete=models.PROTECT)
    final_volume = models.PositiveIntegerField()

    @classmethod
    def make(cls, water, buffer_mix, primers, hgDNA, template, final_volume):
        return MasterMix.objects.create(
            water=water,
            buffer_mix=buffer_mix,
            primers=primers,
            hgDNA=hgDNA,
            template=template,
            final_volume=final_volume,
        )

    @classmethod
    def clone(cls, src):
        return cls.make(
            src.water, # FK ok to inherit ConcreteReagent used by src.
            src.buffer_mix.clone(), # Must get its own BufferMix.
            src.primers.clone(), # Must get its own placeholder reagents.
            src.hgDNA.clone(), # Must get its own placeholder reagents.
            src.template.clone(), # Must get its own placeholder reagents.
            src.final_volume, # Is a plain value, not a relation.
        )
        

