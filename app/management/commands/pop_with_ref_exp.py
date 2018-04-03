from pdb import set_trace as st

from django.core.management.base import BaseCommand

from app.model_builders.make_ref_exp import ReferenceExperiment

class PopWithRefExperiment():

    @classmethod
    def populate(cls):
        ReferenceExperiment().create()


class Command(BaseCommand):
    def handle(self, *args, **options):
        PopWithRefExperiment().populate()
