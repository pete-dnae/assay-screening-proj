import re
import json
from app.model_builders.batch_reagent_entry import BatchReagentEntry

"""
Django *command* that helps you put a batch of reagents into the database in
one go.
    
Takes a CSV file name as a command line parameter, and expects to find 
(reagent + category) contents like this:

    sausage, savoury
    beans, savoury
    apples, fruit

It then uses the BatchReagentEntry class to bulk-load these into the
database. Refer to *BatchReagentEntry* for more detailed usage rules.
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
        rows = []
        for idx, line in enumerate(lines):
            lnum = int(idx) + 1
            line = line.strip()
            if len(line) == 0:
                continue
            if isinstance(line,bytes):
                line = line.decode("utf-8")
            fields = line.split(',')
            cls._assert_three_fields(fields, line, lnum)
            fields = [f.strip() for f in fields]
            for index,field in enumerate(fields):
                cls._assert_no_spaces(field, line, lnum)
                if index == 2:
                    if field !='null':
                        fields[2] = json.dumps({'amplicon_length':field})
                    else:
                        fields[2] = None

            rows.append(fields) # reagent, category
            
        # Use loader to load.
        loader = BatchReagentEntry()
        loader.load_db(rows)

    @classmethod
    def _assert_three_fields(cls, fields, line, lnum):
        if len(fields) == 3:
            return
        raise RuntimeError(
            'Line <%d> (%s), does not have 3 fields.' % (lnum, line))

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

    help = 'Loads reagents in bulk, from CSV file.'

    _CSV_FILE = 'csv_file'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file', type=argparse.FileType(mode='r'))

    def handle(self, *args, **options):
        fd = options[Command._CSV_FILE]
        Loader.load(fd)
