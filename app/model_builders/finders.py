"""
All the db modular entity finders reside here
"""

from app.models.reagent_models import *
from app.models.primer_models import *
from app.models.strain_models import *
from app.models.experiment_model import *
from app.models.rule_models import *

"""
   A few 'finder' methods.
   """



class Finders:

    def __init__(self):
        pass

    @classmethod
    def _conc_rat(cls, denom, numerator, pref_units):
        # Find a Concentration from a rational number (fraction)
        string_value = Concentration.value_from_quotient(denom, numerator)
        return Concentration.objects.get(
            normalised_string_value=string_value, preferred_units=pref_units)

    @classmethod
    def _conc_str(cls, normalised_string_value, pref_units):
        # Find a Concentration from its normalised string value.
        return Concentration.objects.get(
            normalised_string_value=normalised_string_value,
            preferred_units=pref_units)

    @classmethod
    def _org(cls, abbr):
        return Organism.objects.get(abbreviation=abbr)

    @classmethod
    def _arg(cls, name):
        return Arg.objects.get(name=name)

    @classmethod
    def _gene(cls, name):
        return Gene.objects.get(name=name)

    @classmethod
    def _prim(cls, name):
        return Primer.objects.get(full_name=name)

    @classmethod
    def _find_id_primer_pair(cls, fwd_name, rev_name):
        primer_pair = PrimerPair.objects.get(
            forward_primer__full_name=fwd_name,
            reverse_primer__full_name=rev_name,
            suitable_for_id=True,
        )
        return primer_pair

    @classmethod
    def _find_pa_primer_pair(cls, fwd_name, rev_name):
        primer_pair = PrimerPair.objects.get(
            forward_primer__full_name=fwd_name,
            reverse_primer__full_name=rev_name,
            suitable_for_pa=True,
        )
        return primer_pair

    @classmethod
    def _find_primer_pair(cls, fwd_name, rev_name,
                          suitable_for_pa, suitable_for_id):
        primer_pair = PrimerPair.objects.get(
            forward_primer__full_name=fwd_name,
            reverse_primer__full_name=rev_name,
            suitable_for_pa=suitable_for_pa,
            suitable_for_id=suitable_for_id,
        )
        return primer_pair

    @classmethod
    def _reagent(cls, reagent_hash):
        """
        Example reagent_hash could be: 'ATCC 26189:5.000e+01'
        """
        return Reagent.objects.get(hash=reagent_hash)