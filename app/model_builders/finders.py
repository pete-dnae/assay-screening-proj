"""
All the db modular entity finders reside here
"""

from app.models.reagent_models import *
from app.models.primer_models import *
from app.models.strain_models import *
from app.models.experiment_model import *
from app.models.rule_models import *
from app.models.reagent_models import *
"""
   A few 'finder' methods.
   """



class Finders:

    def __init__(self):
        pass




    @classmethod
    def org(cls, abbr):
        return Organism.objects.get(abbreviation=abbr)

    @classmethod
    def arg(cls, name):
        return Arg.objects.get(name=name)

    @classmethod
    def gene(cls, name):
        return Gene.objects.get(name=name)

    @classmethod
    def prim(cls, name):
        return Primer.objects.get(full_name=name)

    @classmethod
    def find_id_primer_pair(cls, fwd_name, rev_name):
        primer_pair = PrimerPair.objects.get(
            forward_primer__full_name=fwd_name,
            reverse_primer__full_name=rev_name,
            suitable_for_id=True,
        )
        return primer_pair

    @classmethod
    def find_pa_primer_pair(cls, fwd_name, rev_name):
        primer_pair = PrimerPair.objects.get(
            forward_primer__full_name=fwd_name,
            reverse_primer__full_name=rev_name,
            suitable_for_pa=True,
        )
        return primer_pair

    @classmethod
    def find_primer_pair(cls, fwd_name, rev_name,
                          suitable_for_pa, suitable_for_id):
        primer_pair = PrimerPair.objects.get(
            forward_primer__full_name=fwd_name,
            reverse_primer__full_name=rev_name,
            suitable_for_pa=suitable_for_pa,
            suitable_for_id=suitable_for_id,
        )
        return primer_pair
    @classmethod
    def find_all_reagents(cls):
        possible_reagent_containers = (PrimerPair,ConcreteReagent,Strain)
        result =[]
        for reagent_container in possible_reagent_containers:
            for object in reagent_container.objects.all():
                result.append(object.__str__())
        return result