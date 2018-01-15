from django.core.management.base import BaseCommand

from .empty_app_tables import EmptyAppTables
from .pop_with_ref_exp import PopWithRefExperiment

class Command(BaseCommand):
    def handle(self, *args, **options):
        EmptyAppTables.empty()
        PopWithRefExperiment.populate()
