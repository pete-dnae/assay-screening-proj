"""
A set of related model classes that help us define reagents.
"""

from django.db import models

from .odds_and_ends_models import mk_choices


class Concentration(models.Model):
    """
    A utility class to encapsulate one particular concentraction value, defined
    as a floating point, volumetric ratio w.r.t. water.

    A concentration also has preferred display units to make the numbers easier
    for humans to read or enter. But internally the value held is
    by-defintion dimensionless.
    """

    presentation_units_choices = mk_choices((
        'X',
        'mM',
        'mg/ml',
        'mM each',
        'microM each',
        'ng/ul',
        'cp/ul',
        '%'))

    value = models.FloatField()
    preferred_units = models.CharField(max_length=15, choices=units_choices)

    @classmethod
    def make(cls, value, preferred_units):
        return Concentration.objects.create(
            value=value, preferred_units=preferred_units)

    @classmethod
    def clone(cls, src):
        return cls.make(src.value, src.preferred_units)


class Reagent(models.Model):
    """
    A prescribed *type* of liquid, that we can go out and procure at a known
    concentration. E.g. a primer, TAQ, a template etc.
    """
    # Note names are not unique, because a different Reagent is defined for
    # each concentration.
    name = models.CharField(max_length=30) 
    lot = models.CharField(max_length=30)
    concentration = models.ForeignKey(
        Concentration, related_name='retgent', on_delete=models.PROTECT)

    @classmethod
    def make(self, name, lot, stock, final, units):
        concentration = Concentration.make(stock, final, units)
        reagent = ConcreteReagent.objects.create(
            name=name, lot=lot, concentration=concentration)
        return reagent


class Composition(models.Model):
    """
    A way to specify the makeup type for a liquid mixture. It is a type for a
    liquid, not the presence, or an instance of some liquid. It lists the
    *Reagent*s the mixture is made up from. (Recall that every Reagent is
    defined with a concentration value.) A Composition does not have a
    volume; it is a type for a thing, not a thing.
    """

    reagents = models.ForeignKey(
        Reagent, related_name='composition', on_delete=models.PROTECT)

    @classmethod
    def make(cls, reagents):
        composition = Composition.objects.create(
        )
        for reagent in reagents:
            composition.reagents.add(reagent)
        composition.save()
        return composition

    @classmethod
    def clone(cls, src):
        return cls.make(
            [Composition.clone(ra) for ra in src.reagents.all()] # New
        )

class Measure(models.Model):
    """
    As in 'A measure of Rum'. A physical, single, tangible, particular
    instance of a volume of some liquid. Is immutable. A glug, a shot, a
    splash. Has a prescribed volume. Has a prescribed Composition. Can only
    meaningfully exist in a container which we can identify. Such as a
    bottle, beaker, tube , well, or chamber. Every Measure has exactly one
    container. Every container has exactly one Measure. The names are in fact
    interchangeable. The logical role of the container is make it possible to
    identify the Measure. To make the Measure *addressable*. For example a
    label on a bottle, or the plate/row/column indices of a chamber.
    """

    # E.g. label on bottle or tube, or the row/column of a well.
    address = models.CharField(max_length=30)

    # We choose (arbitrarily) to use milli-litres as our normalised units for
    # volume here.
    volume_in_ml = models.FloatField()


    @classmethod
    def make(cls, address, volume_in_ml):
        return Measure.objects.create(
            address=address,
            volume_in_ml=volume_in_ml,
        )

    @classmethod
    def clone(cls, src):
        return cls.make(
            src.address,
            src.volume_in_ml,
        )
