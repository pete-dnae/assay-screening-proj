from django.core.management.base import BaseCommand

from app.model_builders.make_simple_experiment import SimpleExperiment

class PopWithSimpleExperiment():

    @classmethod
    def populate(cls):
        SimpleExperiment().create()


class Command(BaseCommand):
    def handle(self, *args, **options):
        PopWithSimpleExperiment().populate()
