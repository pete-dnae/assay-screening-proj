"""
This module contains the principal RuleScriptParser class, in addition to a
dedicated ParseError exception class. Plus some private helper classes.
"""

from pdb import set_trace as st

from collections import OrderedDict
import re

from app.rules_engine.alloc_rule import AllocRule
from app.rules_engine.transfer_rule import TransferRule
from app.rules_engine.transfer_rule import IncompatibleTransferError
from app.rules_engine.row_col_intersections import RowColIntersections
from app.rules_engine.thermal_cycle_rule import ThermalCycleRule


class RuleScriptParser:
    """
    Capable of parsing and validating the rules-script text to produce a
    either a machine-readable, and structured representation, of a 
    successfully validated script, or details about how it fails validation.
    """

    VERSION = "ver-1"  # Language version this parser is for.

    def __init__(self, reagents, units, script):
        """
        Provide in *reagents* a sequence of allowed reagent names. Similarly 
        for *units*. Provide in *script* the input text as one big string.  
        """
        self._available_reagents = reagents
        self._available_units = units
        self._script = script
        self._lines = None

        # State variables to support the parsing operation.
        self._cur_plate = None
        self._version = None
        self._parse_posn = _ParsePosn()  # Position reached in script.
        self._fields = None  # The fields in the current line.

        # self.rule_objects is an OrderedDict keyed on plate name. The
        # values are sequences of mixed AllocRule,TransferRule objects
        # and ThermalCyclingRules.

        self.rule_objects = OrderedDict()

        # self.line_number_mapping provides the the script line number
        # provenance for each rule object in self.rule_objects.
        self.line_number_mapping = {}

    def parse(self):
        """
        If there are syntax errors, raises ParseError. Otherwise,
        populates self.rule_objects and self.line_number_mapping.
        """
        self._lines = self._script.splitlines()

        for line_index, line in enumerate(self._lines):
            self._parse_posn.starting_new_line(line_index, line)
            self._fields = _LineFields(line.split(), self._err)

            if self._comment_or_blank_line():
                continue

            seeking = 'First Letter'
            if self._fields.field(0, seeking) == 'V':
                self._register_version()
            elif self._fields.field(0, seeking) == 'P':
                self._register_plate()
            elif self._fields.field(0, seeking) == 'A':
                alloc_rule = self._parse_allocation_line()
                self.rule_objects[self._cur_plate].append(alloc_rule)
                self.line_number_mapping[alloc_rule] = line_index + 1
            elif self._fields.field(0, seeking) == 'T':
                trans_rule = self._parse_transfer_line()
                self.rule_objects[self._cur_plate].append(trans_rule)
                self.line_number_mapping[trans_rule] = line_index + 1
            elif self._fields.field(0, seeking) == 'C':
                thermal_cycling_rule = self._parse_cycling_line()
                self.rule_objects[self._cur_plate].append(thermal_cycling_rule)
                self.line_number_mapping[thermal_cycling_rule] = line_index + 1
            else:
                self._err('Line must start with one of the letters V|P|A|T|C.')
        if self._version is None:
            self._err('You must specify a version (in the first line).')

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _comment_or_blank_line(self):
        """
        Is the current line either a comment, or entirely whitespace?
        """
        if len(self._parse_posn.line.strip()) == 0:
            return True
        if self._parse_posn.line.startswith('#'):
            return True
        return False

    def _register_version(self):
        """
        Parses and validates a script version line.
        """
        # The version is compulsory, and must be specified in the first line, 
        # and only in the first line. We are able to check only the latter 
        # here.
        if self._parse_posn.line_index != 0:
            self._err('Version must be specified in the first line.')
        version_string = self._fields.field(1, 'Version')
        if version_string != self.VERSION:
            self._err('Your script version is not recognized by this parser.',
                      version_string)
        self._version = version_string

    def _register_plate(self):
        """
        Parses and validates a plate declaration line, then  registers the
        plate name as a key in the results data structure, and that this is 
        now the *current* plate.
        """
        plate_name = self._fields.field(1, 'Plate name')
        self._assert_plate_is_new(plate_name)
        self.rule_objects[plate_name] = []
        self._cur_plate = plate_name

    # todo pch - the comments in this method and the methods for the other two
    # rule types, should not say 'storing the results in...'. They don't take
    # responsibility for the storage any more.
    def _parse_allocation_line(self):
        """
        Parses and validates an 'A' line, and returns a AllocRule Object on
        successful parsing
        """
        self._assert_a_plate_is_defined()

        reagent = self._fields.field(1, 'Reagent')
        # Check the reagent so that any error message about the reagent
        # doesn't get masked by an error about there being too few fields.
        self._assert_reagent_is_known(reagent)

        cols = self._fields.field(2, 'Columns specification')
        rows = self._fields.field(3, 'Rows specification')
        conc = self._fields.field(4, 'Concentration')

        units = self._fields.field(5, 'Concentration units')
        self._assert_units_are_known(units)

        rows = self._parse_row_spec(rows)
        cols = self._parse_col_spec(cols)
        conc_value = self._parse_conc_value(conc)
        conc_units = units

        return AllocRule(reagent, RowColIntersections(rows, cols),
                         conc_value, units)

    def _parse_cycling_line(self):
        """
        Parses and validates a 'C' line, and returns a ThermalCyclingRule
        Object on successful parsing
        """
        self._assert_a_plate_is_defined()

        temperature_steps = self._fields.field(1, 'temperature steps')
        temperature_steps = self._parse_thermal_cycle_steps(temperature_steps)
        cycle = self._fields.field(2, 'repeat cycle')
        self._assert_repeat_cycle_is_valid(cycle)
        unit = self._fields.field(3, 'x')
        self._assert_thermal_cycling_unit(unit)
        return ThermalCycleRule(temperature_steps, cycle, unit)

    def _parse_thermal_cycle_steps(self, steps):
        """
        Verifies if instructions for thermal cycling
        is a comma separated strings of temperature and time combination

        A temperature and time combination should be represented in below format

         time@temperature
            ex : 10@95 meaning ten seconds at 95 degree centigrade
        """
        m = _THERMAL_CYCLING_STEPS_RE.match(steps)

        if m is None:
            self._err('Incorrect format for steps expected time@temp,time@temp...', steps)

        steps_as_list = steps.split(',')
        steps_as_instructions = ''
        for entity in steps_as_list:
            time, temp = entity.split('@')
            steps_as_instructions += ('%sSec at %s°C, ' % (time, temp))

        return steps_as_instructions

    def _assert_repeat_cycle_is_valid(self, cycle):
        """
        Demands that the cycle number provided in thermal cycling is an integer
        """
        try:
            return int(cycle)
        except ValueError:
            self._err('cycle is not a valid integer', cycle)


    def _assert_thermal_cycling_unit(self, unit):
        """
        Demands that the unit mentioned in thermal cycling rule is x
        """

        if unit != 'x':
            self._err('Number of cycles should be followed by x', unit)

    def _parse_transfer_line(self):
        """
        Parses and validates a 'T' line, storing the results in the results
        in self.rule_objects.
        """
        self._assert_a_plate_is_defined()

        # Variable naming...
        # s_ for source, d_ for destination

        s_plate = self._fields.field(1, 'Source plate name')
        self._assert_plate_is_known(s_plate)
        self._assert_plate_is_not_current(s_plate)
        s_cols = self._fields.field(2, 'Source columns')
        s_rows = self._fields.field(3, 'Source rows')
        d_cols = self._fields.field(4, 'Desination columns')
        d_rows = self._fields.field(5, 'Desination rows')
        conc = self._fields.field(6, 'Concentration')

        units = self._fields.field(7, 'Concentration units')
        self._assert_units_is_dilution(units)

        s_rows = self._parse_row_spec(s_rows)
        s_cols = self._parse_col_spec(s_cols)
        d_rows = self._parse_row_spec(d_rows)
        d_cols = self._parse_col_spec(d_cols)
        conc_value = self._parse_conc_value(conc)
        conc_units = units

        # The TransferRule constructor raises exceptions if the source and 
        # destination row/columns are incompatible shapes.
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
        known_plates = self.rule_objects.keys()
        if plate_name in known_plates:
            self._err('This plate name been used before.', plate_name)

    def _assert_plate_is_known(self, plate_name):
        """
        Demands tha the plate name is one of those captured earlier from
        a plate declaration.
        """
        if plate_name not in self.rule_objects.keys():
            self._err('Transfer from unknown plate', plate_name)

    def _assert_plate_is_not_current(self,plate_name):
        """
        Demands that the transfer rule does not refer to the current plate
        """
        if plate_name == self._cur_plate:
            self._err('Transfer from same plate is not allowed',plate_name)

    def _assert_reagent_is_known(self, reagent):
        """
        Demands tha the reagent is one of the reagenets provided at
        construction time as *allowed*.
        """
        if reagent in self._available_reagents:
            return
        self._err('Unknown reagent.', reagent)

    def _assert_units_are_known(self, units):
        """
        Demands tha the units is one of the units strings provided at
        construction time as *allowed*.
        """
        if units in self._available_units:
            return
        self._err('Unknown units.', units)

    def _assert_units_is_dilution(self, conc_units):
        """
        Demands that the units is 'dilution'
        """
        if conc_units != 'dilution':
            self._err('Units for a transfer must be <dilution>.', conc_units)

    def _parse_col_spec(self, cols_spec):
        """
        Interprets (with error handling) strings like these.
        '1-12' or '3,4,5', or '3'
        Returns a flat list of the column numbers thus represented.
        """
        # Range?
        m = _INT_RANGE_RE.match(cols_spec)
        if m is not None:
            start, end = m.group(1, 2)
            as_list = [str(x) for x in range(int(start), int(end) + 1)]

        # Discrete list?
        elif ',' in cols_spec:
            as_list = cols_spec.split(',')

        # Must now be single value
        else:
            as_list = (cols_spec,)
        # Convert to integers - noting that this is still vulnerable to
        # letters being present in some cases..
        try:
            as_list = [int(s) for s in as_list]
        except ValueError:
            self._err('Struggling with a non-number in columns specification.',
                      cols_spec)
        return as_list

    def _parse_row_spec(self, rows_spec):
        """
        Interprets (with error handling) strings like these.
        'A-F' or 'A,B,C', or 'C'
        Returns a flat list of the row letters thus represented - BUT NOT 
        as letters; instead the letters are converted to integers starting with
        1 for 'A'. (Anticipating downstream use of RowColIntersection class.)
        """
        # Range?
        m = _LETTER_RANGE_RE.match(rows_spec)
        if m is not None:
            start, end = m.group(1, 2)
            as_list = [chr(x) for x in range(ord(start), ord(end) + 1)]

        # Discrete list?
        elif ',' in rows_spec:
            as_list = rows_spec.split(',')
            self._assert_letters(as_list, rows_spec)

        # Must now be single value
        else:
            as_list = rows_spec,
            self._assert_letters(as_list, rows_spec)
        return [1 + ord(c) - ord('A') for c in as_list]

    def _parse_conc_value(self, conc):
        """
        Parses and validates a concentration value. Returns a float.
        """
        try:
            return float(conc)
        except ValueError:
            self._err('Cannot convert concentration to a number.', conc)

    def _assert_letters(self, seq, source_string):
        """
        Demand that all the strings provided in *seq* are capital letters.
        """
        for item in seq:
            if not item:
                self._err('Empty item in rows specification Hint: do not leave trailing commas',
                          source_string)
            if item not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                self._err('Only uppercase letters allowed in rows specification.',
                          source_string)

    def _err(self, basic_message, culprit_string=None):
        """
        Raises ParseError, having automatically appended parsing position info 
        to the basic_message..

        The *culprit_string* parameter is optional. When you provide a non
        empty one, this will be included in the error message.
        """
        # Add line number to the error message.
        basic_message += (' Line %d.' % (self._parse_posn.line_index + 1))
        if culprit_string:
            basic_message += ' Culprit: (%s).' % culprit_string

        position_in_script = self._chars_in_script_preceding(
            self._parse_posn.line_index)

        raise ParseError(basic_message, position_in_script)

    def _chars_in_script_preceding(self, line_index):
        """
        How many characters are there in the script before the given line?
        This includes the newlines at the end of the preceding lines.
        """
        count = 0
        for line in self._lines[:line_index]:
            count += len(line) + 1
        return count


class _ParsePosn():
    """
    Models how far through the script the parser has reached - mainly for
    error reporting.
    """

    def __init__(self):
        self.line_index = None  # Line number, but zero-based.
        self.line = None  # Line contents.

    def starting_new_line(self, line_index, line):
        """
        Mandate to update the parse position to the start of a new line.
        """
        self.line_index = line_index
        self.line = line


class _LineFields():
    """
    Models the fields in a line. Just a list - but with some convenience
    methods.
    """

    def __init__(self, strings, error_fn_callback):
        """
        Provide the field strings as a sequence.
        Provide an error handling callback that takes a single (string) message 
        argument.
        """
        self.strings = strings
        self._error_callback_fn = error_fn_callback

    def field(self, field_index, name):
        """
        Returns the n'th field inside self._fields if there is one.
        (Zero-based). Otherwise calls your error reporting callback with a
        message including the field name string passed in.
        """
        # Too few fields present?
        if field_index >= len(self.strings):
            field_num = field_index + 1  # Human 1-based.
            self._error_callback_fn(
                'Field number %d (%s) is missing.' % (field_num, name))
        return self.strings[field_index]


class ParseError(Exception):
    """
    A simple Exception that carries a message about a parsing error, and also
    whereabouts in the script that error occurs. 
    """

    def __init__(self, message, where_in_script):
        """
        The *where_in_script* parameter should be the index into the
        entire script of the character the user should be directed to as the
        location of the error. (To help GUI editors).
        """
        self.message = message
        self.where_in_script = where_in_script


_INT_RANGE_RE = re.compile(r'(\d+)-(\d+)$')
_LETTER_RANGE_RE = re.compile(r'([A-Z])-([A-Z])$')
_THERMAL_CYCLING_STEPS_RE = re.compile(r'^(\d+@\d+)(,\s*\d+@\d+)*$')
