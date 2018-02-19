from django.core.management.base import BaseCommand

from .empty_app_tables import EmptyAppTables
from .pop_with_simple_exp import PopWithSimpleExperiment

class Command(BaseCommand):
    def handle(self, *args, **options):
        EmptyAppTables.empty()
        PopWithSimpleExperiment.populate()
