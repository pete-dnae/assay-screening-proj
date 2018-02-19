
from app.models.reagent_models import *
from app.models.primer_models import *
from app.models.strain_models import *
from app.models.experiment_model import *
from app.models.plate_models import *
from .finders import Finders


class CreateExperiment:

    def __init__(self):
        pass

    @classmethod
    def _create_pa_cycling(cls):
        return CyclingPattern.make(
            activation_time=120,
            activation_temp=95,
            num_cycles=20,
            denature_time=10,
            denature_temp=95,
            anneal_time=10,
            anneal_temp=62,
            extend_temp=72,
            extend_time=30
        )

    @classmethod
    def _create_id_cycling(cls):
        return CyclingPattern.make(
            activation_time=120,
            activation_temp=95,
            num_cycles=20,
            denature_time=10,
            denature_temp=95,
            anneal_time=0,
            anneal_temp=0,
            extend_temp=62,
            extend_time=25
        )

    @classmethod
    def _create_concentrations(cls):
        for denom, numerator, pref_units in (
                (1,0.4, 'microM'),
                (1, 1, 'X'),
                (10, 0.13, 'X'),
                (10, 0.2, 'mM'),
                (10, 0.04, '%'),
                (20, 1, 'mg/ml'),
                (25, 2.06, 'mM'),
                (50, 1.0, 'x'),
                (50, 1.3, 'x'),
                (100, 0.32, 'X'),
                (100, 1, 'mM'),
                (1000, 48, 'mM')):
            Concentration.make(numerator / float(denom), pref_units)

    @classmethod
    def _rules_from_data(cls, payload_type, data):
        rules = []
        for i,rule in enumerate(data):
            payload, zone = rule
            rules.append(AllocRule.make(i,
                payload_type, payload, zone))
        return rules

