from django.core.management.base import BaseCommand

from app.models.experiment_model import *
from app.models.rules_script_model import *
from app.models.reagent_name_model import *
from app.models.units_model import *

# This list has to be in dependency order.
# If A refers to B with a foreign key, then the A must be deleted first.

_APP_MODEL_CLASSES = (
    ExperimentModel,
    RulesScriptModel,
    ReagentNameModel,
    UnitsModel,
)

class EmptyAppTables():

    @classmethod
    def empty(cls):
        for model_class in _APP_MODEL_CLASSES:
            model_class.objects.all().delete()


class Command(BaseCommand):
    def handle(self, *args, **options):
        EmptyAppTables.empty()
