"""
A set of related classes that help us define reagents.
"""

from app.models.odds_and_ends_models import mk_choices


class Concentration:
    """
    A utility class to encapsulate one particular concentration value, defined
    as a floating point, volumetric ratio of some unspecified / arbitrary liquid,
    w.r.t. water.

    A concentration also has preferred display units to make the numbers easier
    for humans to read or enter. But internally the value held is
    by-defintion dimensionless.

    We hold the value as a carefully formatted string, to make it more easily
    hashable, and resilient to rounding differences when calculated in diverse
    ways.
    """
    def __init__(self,conc,units):

        # normalised string E.g. '1.235e+08'
        # See normalised() method.
        self.normalised_string_value = self._normalised(conc)
        self.numerical_value = conc
        self.preferred_units = units

    @classmethod
    def value_from_quotient(cls, denom, numerator):
        return cls._normalised(numerator / denom)

    @classmethod
    def _normalised(cls, numerical_value):
        return '%.3e' % numerical_value



class Reagent:
    """
    A prescribed *type* of liquid, that we can go out and procure at a known
    concentration. E.g. a primer, TAQ, a template etc.
    """
    # Note names are not unique, because a different Reagent is defined for
    # each concentration.
    def __init__(self,name,conc,units):
        self.name = name
        self.concentration = Concentration(conc,units)

    def __hash__(self):
        return self.make_hash(self.name, self.concentration.normalised_string_value)

    def __str__(self):
        return self.name +" "+ self.concentration.normalised_string_value +" "+self.concentration.preferred_units

    @staticmethod
    def make_hash( reagent_name,conc_normalised_string):
        return hash(reagent_name+':'+conc_normalised_string)


