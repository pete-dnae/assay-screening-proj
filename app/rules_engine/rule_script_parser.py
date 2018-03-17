from collections import OrderedDict
import re
from pdb import set_trace as st

from app.rules_engine.alloc_rule import AllocRule
from app.rules_engine.transfer_rule import TransferRule
from app.rules_engine.transfer_rule import IncompatibleTransferError
from app.rules_engine.row_col_intersections import RowColIntersections

class ParseError(Exception):

    def __init__(self, message, where_in_script):
        """
        The *where_in_script* parameter should be the index into the
        entire script of the character the user should be directed to as the
        location of the error. (To help GUI editors).
        """
        super().__init__(message)
        self._where_in_script = where_in_script

    def __str__(self):
        return super().__str__() + (', at index: %d' % self._where_in_script)


class RuleScriptParser:
    """
    Capable of parsing and validating the rules-script text to produce a
    machine readable, and structured representation..
    """

    VERSION = "ver-1" # Language version this parser is for.

    def __init__(self, reagents, units, script):
        """
        Provide in *reagents* a sequence of allowed reagent names.
        Similarly for *units*.  Provide in *script* the input text as one big
        string.  
        """
        self._available_reagents = reagents
        self._available_units = units
        self._script = script
        self._cur_plate = None
        self._version = None

        self._parse_posn = _ParsePosn()
        self._fields = None # Is-a _LineFields

        self.results = OrderedDict()


    def parse(self):
        """
        If there are syntax errors, raises ParseError. Otherwise,
        populates self.results - an OrderedDict keyed on plate name.  The
        values are sequences of mixed AllocRule and TransferRule objects.
        """
        lines = self._script.splitlines()

        for line_index, line in enumerate(lines):
            self._parse_posn.starting_new_line(line_index, line)
            self._fields = _Fields(self.line.split())

            if self._comment_or_blank_line():
                continue

            # todo demand on line number 1 that is good version line
            # then continue

            # todo after that regard V as unknown line type

            seeking = 'First Letter'
            if self._fields.field(0, seeking) == 'P':
                self._register_plate()
            elif self._fields.field(0, seeking) == 'A':
                alloc_rule = self._parse_alloc_line()
                self.results[self._cur_plate].append(alloc_rule)
            elif self._fields.field(0, seeking) == 'T':
                trans_rule = self._parse_transfer_line()
                self.results[self._cur_plate].append(trans_rule)
            else:
                self._err('Line must start with one of the letters A|T|P")

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _comment_or_blank(self):
        if len(self._parse_posn.line.strip()) == 0:
            return True
        if self._parse_posn.line.startswith('#'):
            return True
        return False

    def _register_plate(self, fields):
        """
        Parses and validates a plate declaration line, then  registers the
        plate name as a key in the results data structure, and that this is 
        now the *current* plate.
        """
        plate_name = self._fields.field(1, 'Plate name')
        self._assert_plate_is_new(plate_name)
        self.results[plate_name] = []
        self._cur_plate = plate_name

    def _parse_allocation_line(self):
        """
        Parses and validates an 'A' line, storing the results in the results
        in self.results.
        """
        self._assert_a_plate_is_defined()

        reagent = self._fields.field(1, 'Reagent')
        rows = self._fields.field(2, 'Rows specification')
        cols = self._fields.field(3, 'Columns specification')
        conc = self._fields.field(4, 'Concentration')
        units = self._fields.field(5, 'Concentration units')

        self._assert_reagent_is_known(reagent)
        rows = self._parse_row_spec(rows)
        cols = self._parse_col_spec(cols)
        conc_value = self._parse_conc_value(conc)
        conc_units = units

        self._assert_units_are_known(units)

        return AllocRule(reagent, RowColIntersections(rows, cols), 
                conc_value, units)

    def _parse_T_line(self, fields):
        """
        Parses and validates a 'T' line, storing the results in the results
        in self.results.
        """
        self._assert_a_plate_is_defined()
        # s for source, d for destination

        s_plate = self._fields.field(1, 'Source plate name')
        s_rows = self._fields.field(2, 'Source rows')
        s_cols = self._fields.field(3, 'Source columns')
        conc = self._fields.field(4, 'Concentration')
        units = self._fields.field(5, 'Concentration units')

        self._assert_plate_is_known(s_plate)

        s_rows = self._parse_row_spec(s_rows)
        s_cols = self._parse_col_spec(s_cols)
        d_rows = self._parse_row_spec(d_rows)
        d_cols = self._parse_col_spec(d_cols)
        conc_value = self._parse_conc_value(conc)
        conc_units = units

        self._assert_units_is_dilution(conc_units)

        # The TransferRule raises exceptions if the source and destination
        # row/columns are incompatible shapes.
        try:
            t_rule = TransferRule(s_plate, 
                RowColIntersections(s_rows, s_cols), 
                RowColIntersections(d_rows, d_cols), conc_value)
        except IncompatibleTransferError:
            self._err('Shape of source rows/columns is incompatible with ' + \
                    'that of destination.')
        return t_rule

    def _assert_a_plate_is_defined(self):
        """
        Demands that a *current* plate is defined in the parser state.
        """
        if self._cur_plate is None:
            self._err('You must define a plate before this.')

    def _assert_plate_is_new(self, plate_name):
        """
        Demands that this plate name has not been declared earlier in the
        script.
        """
        known_plates = self.results.keys()
        if plate_name in known_plates:
            self._err('This plate name been used before.', plate_name)

    def _assert_plate_is_known(self, plate_name):
        """
        Demands tha the plate name is one of those captured earlier from
        a plate declaration.
        """
        return plate_name in self.results.keys()

    def _assert_reagent_is_known(self, reagent):
        """
        Demands tha the reagent is one of the reagenets provided at
        construction time as *allowed*.
        """
        if reagent in self._available_reagents:
            return
        self._err('Unknown reagent', reagent)

    def _assert_units_are_known(self, units):
        """
        Demands tha the units is one of the units strings provided at
        construction time as *allowed*.
        """
        if units in self._available_units:
            return
        self._err('Unknown units', units)


    def _assert_units_is_dilution(self, conc_units):
        """
        Demands that the units is 'dilution'
        """
        if conc_units != 'dilution':
            self._err('Units for a transfer must be <dilution>', conc_units)

    def _parse_row_spec(self, rows_spec):
        """
        Interprets (with error handling) strings like these.
        '1-12' or '3,4,5', or '3'
        Returns a flat list of what they represent. (As integers).
        """
        # Range?
        m = _INT_RANGE_RE.match(rows_spec)
        if m is not None:
            start, end = m.group(1,2)
            as_list = [str(x) for x in range(int(start), int(end)+1)]

        # Discrete list?
        elif ',' in rows_spec:
            as_list = rows_spec.split(',')

        # Must now be single value
        else:
            as_list = (rows_spec,)
        try:
            as_list = [int(s) for s in as_list]
        except ValueError:
            self._err('Struggling with a non-number in rows specification', 
                    rows_spec)
        return as_list

    def _parse_col_spec(self, cols_spec):
        """
        Interprets (with error handling) strings like these.
            'A-F' or 'A,B,C', or 'C'
        Returns a flat list of the letters that they represent - BUT NOT as
        letters; instead the letters are converted to integers starting with
        1 for 'A'.
        """
        # Range?
        m = _LETTER_RANGE_RE.match(cols_spec)
        if m is not None:
            start, end = m.group(1,2)
            as_list = [chr(x) for x in range(ord(start), ord(end)+1)]

        # Discrete list?
        elif ',' in cols_spec:
            as_list = cols_spec.split(',')
            self._assert_letters(as_list, cols_spec)

        # Must now be single value
        else:
            as_list = cols_spec,
            self._assert_letters(as_list, cols_spec)
        return [1 + ord(c) - ord('A') for c in as_list]

    def _parse_conc_value(self, conc):
        """
        Parses and validates a concentration value. Returns a float.
        """
        try:
            return float(conc)
        except ValueError:
            self._err('Cannot convert concentration to a number', conc)

    def _assert_letters(self, seq, source_string):
        """
        Demand that all the strings provided in *seq* are capital letters.
        """
        for item in seq:
            if item not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                self._err('Only letters allowed in columns specification', 
                        source_string)

    def _err(self, basic_message, culprit_string=None):
        """
        Raises ParseError, having automatically added parsing position info.

        The *culprit_string* parameter is optional. When you provide a non
        empty one, this will be included in the error message, and it will also
        be used to deduce whereabouts on the line the error occurs so this also
        can be reported..
        """
        # Add line number to the error message.
        basic_message += (' Line %d.' % self._parse_posn.line_index + 1)

        position_in_script = self._chars_in_script_preceding(
                self._parse_posn.line_index)

        # If *culprit_string* is given, we can add a character number too.
        if culprit_string:
            index_in_line = self._parse_posn.line.find(sub)
            basic_message += ' Character %d.' % (index_in_line + 1)
            position_in_script = position_in_script + index_in_line

        raise ParseError(basic_message, position_in_script)


class _ParsePosn():
    """
    Models how far through the script the parser has reached - mainly for
    error reporting.
    """

    def __init__(self):
        self.line_index = None # Zero based.
        self.line = None # Line contents

    def starting_new_line(self, line_index, line):
        self.line_index = lnum
        self.line = line


class _LineFields():
    """
    Models the fields in a line.
    """

    def __init__(self, strings):
        self.strings = strings

    def field(self, field_index, name):
        """
        Provides the n'th field inside self._fields if there is one.
        (Zero-based). Otherwise raises ParseError, including the name string 
        passed in.
        """
        the_string = self._fields.strings.get(n, None)
        if the_string is not None:
            return the_string

        self._err(
            'Field number %d (%s) is missing' % \ 
                    (field_num, name_of_field_for_error_report))

_WORD_RE = re.compile(r'\S+')
_INT_RANGE_RE =re.compile(r'(\d+)-(\d+)$')
_LETTER_RANGE_RE =re.compile(r'([A-Z])-([A-Z])$')
