from django.core.management.base import BaseCommand

from app.models.experiment_model import *
from app.models.reagent_models import *
from app.models.primer_models import *
from app.models.strain_models import *
from app.models.plate_models import *

# This list has to be in dependency order.
# If A refers to B with a foreign key, then the A must be deleted first.

_APP_MODEL_CLASSES = (
    Experiment,
    
    CyclingPattern,

    Plate,
    AllocationInstructions,
    RuleList,
    AllocRule,

    PrimerPair,
    Primer,

    Strain,
    Organism,
    Gene,
    Arg,

    Measure,
    Composition,
    Reagent,
    Concentration,
)

class EmptyAppTables():

    @classmethod
    def empty(cls):
        for model_class in _APP_MODEL_CLASSES:
            model_class.objects.all().delete()


class Command(BaseCommand):
    def handle(self, *args, **options):
        EmptyAppTables.empty()
