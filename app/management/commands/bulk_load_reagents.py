from pdb import set_trace as st

import argparse

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

class BulkLoadReagents():

    @classmethod
    def load(cls, fd):
        # parse file into ds required for loader
        # use loader to load
        pass


class Command(BaseCommand):

    help = 'Loads reagents in bulk, from CSV file.'

    _CSV_FILE = 'csv_file'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', dest=Command._CSV_FILE, type=argparse.FileType(mode='r'))

    def handle(self, *args, **options):
        fd = options[Command._CSV_FILE]
