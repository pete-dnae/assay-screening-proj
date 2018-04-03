from collections import defaultdict
import re

from app.model_builders.batch_groups_entry import BatchGroupsEntry

"""
Django *command* that helps you put a batch of reagent groups into the database 
in one go.
    
Takes a CSV file name as a command line parameter, and expects to find 
contents like this:

    pool_1, sausage, 0.4, M/uL
    pool_1, beans,   0.1, M/uL
    pool_1, sausage, 0.8, M/uL
    pool_1, beans,   0.2, M/uL

It then uses the BatchGroupEntry class to bulk-load these into the
database. Refer to *BatchGroupEntry* for more detailed usage rules.
"""

from pdb import set_trace as st

import argparse

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

class Loader():
    """
    The class that actually does the work.
    """

    @classmethod
    def load(cls, fd):
        """
        Provide (in fd), a pre-opened file descriptor.
        """
        # Parse and validate input.
        lines = fd.readlines()
        groups = defaultdict(list)
        for idx, line in enumerate(lines):
            lnum = int(idx) + 1
            line = line.strip()
            if len(line) == 0:
                continue
            fields = line.split(',')
            cls._assert_four_fields(fields, line, lnum)
            fields = [f.strip() for f in fields]
            for field in fields:
                cls._assert_no_spaces(field, line, lnum)
            group, reagent, conc, units = fields
            payload = (reagent, conc, units)
            groups[group].append(payload)

        # Use loader to load.
        loader = BatchGroupsEntry()
        loader.load_db(groups)

    @classmethod
    def _assert_four_fields(cls, fields, line, lnum):
        if len(fields) == 4:
            return
        raise RuntimeError(
            'Line <%d> (%s), does not have 4 fields.' % (lnum, line))

    @classmethod
    def _assert_no_spaces(cls, field, line, lnum):
        if re.match(r'^\S+$', field):
            return
        raise RuntimeError(
            'This field: <%s>, on line number %d contains a space.' % 
                (field, lnum))


class Command(BaseCommand):
    """
    The Django management command wrapper. Includes automated command line
    argument validation and parsing.
    """

    help = 'Loads groups in bulk, from CSV file.'

    _CSV_FILE = 'csv_file'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file', type=argparse.FileType(mode='r'))

    def handle(self, *args, **options):
        fd = options[Command._CSV_FILE]
        Loader.load(fd)
