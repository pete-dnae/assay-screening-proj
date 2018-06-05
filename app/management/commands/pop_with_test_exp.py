from pdb import set_trace as st

from django.core.management.base import BaseCommand

from app.model_builders.make_test_experiment import make_test_experiment

class PopWithTestExperiment():

    @classmethod
    def populate(cls):
        make_test_experiment()


class Command(BaseCommand):
    def handle(self, *args, **options):
        PopWithTestExperiment().populate()
