from collections import OrderedDict
import re
from pdb import set_trace as st

from app.rules_engine.alloc_rule import AllocRule
from app.rules_engine.transfer_rule import TransferRule
from app.rules_engine.transfer_rule import IncompatibleTransferError
from app.rules_engine.row_col_intersections import RowColIntersections

class ParseError(Exception):

    def __init__(self, message, line_number):
        super().__init__(message)
        self._line_number = line_number

    def __str__(self):
        return super().__str__() + (', at line: %d' % self._line_number)



class RuleScriptParser:
    """
    Capable of parsing and validating the rules-script text to produce a
    machine readable, and structured representation..
    """

    VERSION = "ver-1" # Language version this parser is for.

    def __init__(self, reagents, units, script):
        """
        Inputs:
        Provide in *reagents* a sequence of allowed reagent names.
        Similarly for *units*.
        Provide in *script* the input text as one big string.

        Outputs:
        Populates self.results - an OrderedDict keyed on plate name.
        The values are sequences of mixed AllocRule and TransferRule 
        objects. 
        """
        self._available_reagents = reagents
        self._available_units = units
        self._script = script
        self._cur_plate = None
        self._lnum = None
        self._version = None
        self.results = OrderedDict()

    def parse(self):
        """
        If the input is legitimate, runs to completion and populates
        self.results. Else raises ParseError.
        """
        lines = self._script.splitlines()
        self._lnum = 1
        self._assert_version_in_first_line(lines)

        for i, line in enumerate(lines):
            self._lnum = i + 2
            if self._comment_or_blank(line):
                continue
            first_field, all_fields = self._extract_fields(line)
            if first_field == 'V':
                continue
            if first_field == 'P':
                self._register_plate(all_fields)
            elif first_field == 'A':
                alloc_rule = self._parse_A_line(all_fields)
                self.results[self._cur_plate].append(alloc_rule)
            elif first_field == 'T':
                trans_rule = self._parse_T_line(all_fields)
                self.results[self._cur_plate].append(trans_rule)
            else:
                self._err('Invalid rule type')

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _comment_or_blank(self, line):
        if len(line.strip()) == 0:
            return True
        if line.startswith('#'):
            return True
        return False

    def _register_plate(self, fields):
        """
        Parses and validates a plate declaration line, then  registers the
        plate name as a key in the results data structure, and that this is 
        now the *current* plate.
        """
        self._assert_there_are_n_fields(fields, 2)
        plate_name = fields[1]
        self._assert_plate_is_new(plate_name)
        self.results[plate_name] = []
        self._cur_plate = plate_name

    def _parse_A_line(self, fields):
        """
        Parses and validates an 'A' line, storing the results in the results
        in self.results.
        """
        self._assert_a_plate_is_defined()
        self._assert_there_are_n_fields(fields, 6)
        letter, reagent, rows, cols, conc, units = fields
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
        self._assert_a_plate_is_defined()
        self._assert_there_are_n_fields(fields, 8)
        # s for source, d for destination
        letter, s_plate, s_rows, s_cols, d_rows, d_cols, conc, units = fields
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
                RowColIntersections(d_rows, d_cols), conc_value, units)
        except IncompatibleTransferError:
            self._err('Shape of source rows/columns is incompatible with ' + \
                    'that of destination')
        return t_rule

    def _assert_version_in_first_line(self, lines):
        """
        Demands that the first line in the script is a version declaration, 
        and that the version matches with the version this parser is written
        for.
        """
        if len(lines) == 0:
            self._err('No lines present in input')
        first_field, all_fields = self._extract_fields(lines[0])
        if first_field != 'V':
            self._err('First line must start with V for version.')
        if len(all_fields) != 2:
            self._err('Too few fields in version line')
        version_string = all_fields[1]
        if version_string  != RuleScriptParser.VERSION:
            self._err('Your version <%s> not supported with this parser' %  \
                    version_string)

    def _assert_a_plate_is_defined(self):
        """
        Demands that a *current* plate is defined in the parser state.
        """
        if self._cur_plate is None:
            self._err('No plate is defined yet')

    def _assert_plate_is_new(self, plate_name):
        """
        Demands that this plate name has not been declared earlier in the
        script.
        """
        known_plates = self.results.keys()
        if plate_name in known_plates:
            self._err('Plate name been used before (%s)' % plate_name)

    def _assert_plate_is_known(self, plate_name):
        """
        Demands tha the plate name is one of those captured earlier from
        a plate declaration.
        """
        return plate_name in self.results.keys()

    def _assert_there_are_n_fields(self, fields, n):
        """
        Demands that there the number of fields present is <n>.
        """
        found = len(fields)
        if len(fields) != n:
            self._err('Should be %d fields, not %d' % (n, found))


    def _assert_reagent_is_known(self, reagent):
        """
        Demands tha the reagent is one of the reagenets provided at
        construction time as *allowed*.
        """
        if reagent in self._available_reagents:
            return
        self._err('Unknown reagent <%s>' % reagent)

    def _assert_units_are_known(self, units):
        """
        Demands tha the units is one of the units strings provided at
        construction time as *allowed*.
        """
        if units in self._available_units:
            return
        self._err('Unknown units <%s>' % units)


    def _assert_units_is_dilution(self, conc_units):
        """
        Demands that the units is 'dilution'
        """
        if conc_units != 'dilution':
            self._err('Units for a transfer must be <dilution>')

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
            self._err('Problem with int() conversion in: <%s>' % rows_spec)
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
            self._err('Problem with float() conversion in: <%s>' % conc)

    def _extract_fields(self, line):
        """
        Separates the lines into fields and provides (as 2 returned values),
        the first field, and then all-fields.
        """
        fields = line.split()
        if len(fields) == 0:
            self._err('No fields to split')
        return fields[0], fields


    def _assert_letters(self, seq, source_string):
        for item in seq:
            if item not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                self._err('Only letters allowed: <%s>' % source_string)

    def _err(self, message):
        """
        Raises ParseError, having furnished line number.
        """
        raise ParseError(message, self._lnum)


_INT_RANGE_RE =re.compile(r'(\d+)-(\d+)$')
_LETTER_RANGE_RE =re.compile(r'([A-Z])-([A-Z])$')
