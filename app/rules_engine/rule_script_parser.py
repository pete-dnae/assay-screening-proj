from collections import OrderedDict
import re
from pdb import set_trace as st

from app.rules_engine.alloc_rule import AllocRule
from app.rules_engine.alloc_rule import TransferRule

class ParseError(Exception):
    """
    Exists only to provide a specific type to try/catch. Offers nothing more
    than <Exception>.
    """
    pass


class RuleScriptParser:
    """
    Capable of parsing and validating the rules-script text.
    """

    VERSION = "ver-1"

    def __init__(self, reagents, units, script):
        """
        Provide in *reagents* a sequence of allowed reagent names.
        Similarly for *units*.
        Provide in *script* the input text as one big string.
        """
        self._available_reagents = reagents
        self._available_units = units
        self._script = script
        self._cur_plate = None
        self._lnum = None
        self._version = None
        # The results objec is an OrderedDict keyed on plate name.
        # The values are sequences of mixed AllocRule and TransferRule 
        # objects. 
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
        return results

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
        self._assert_there_are_n_fields(fields, 2)
        plate_name = fields[1]
        self._assert_plate_is_new(plate_name)
        self.results[plate_name] = []
        self._cur_plate = plate_name

    def _parse_A_line(self, fields):
        self._assert_a_plate_is_defined()
        self._assert_there_are_n_fields(fields, 6)
        letter, reagent, cols, rows, conc, units = fields
        self._assert_reagent_is_known(reagent)
        cols = self._parse_column_spec(cols)
        rows = self._parse_row_spec(rows)
        conc_value = self._parse_conc_value(conc)
        conc_units = units
        self._assert_units_are_known(units)
        return AllocRule(reagent, cols, rows, conc, units)

    def _parse_T_line(self, fields):
        self._assert_a_plate_is_defined()
        self._assert_a_plate_is_defined()
        self._assert_there_are_n_fields(fields, 8)
        # s for source, d for destination
        letter, s_plate, s_cols, s_rows, \
            d_cols, d_rows, conc, units = fields
        self._assert_plate_is_known(s_plate)
        self._assert_source_dest_compatibility(s_cols, s_rows, d_cols, d_rows)
        s_cols = self._parse_column_spec(s_cols)
        s_rows = self._parse_row_spec(s_cols)
        d_cols = self._parse_column_spec(d_cols)
        d_rows = self._parse_row_spec(d_cols)
        conc_value = self._parse_conc_value(conc)
        conc_units = units
        self._assert_units_is_dilution(conc_units)
        return TransferRule(source_plate, s_cols, s_rows, 
                d_cols, d_rows, conc, units)

    def _assert_version_in_first_line(self, lines):
        if len(lines) == 0:
            self._err('No lines present in input', lnum=0)
        first_field, all_fields = self._extract_fields(lines[0])
        if first_field != 'V':
            self._err('First line must start with V for version.')
        version_string = all_fields[1]
        if version_string  != RuleScriptParser.VERSION:
            self._err('Your version <%s> not supported with this parser' %  \
                    version_string)

    def _assert_a_plate_is_defined(self):
        if self._cur_plate is None:
            self._err('No plate is defined yet')

    def _assert_plate_is_new(self, plate_name):
        known_plates = self.results.keys()
        if plate_name in known_plates:
            self._err('Plate name been used before (%s)' % plate_name)

    def _assert_plate_is_known(self, plate_name):
        return plate_name in self.results.keys()

    def _assert_there_are_n_fields(self, fields, n):
        found = len(fields)
        if len(fields) != n:
            self._err('Should be %d fields, not %d' % (n, found))


    def _assert_reagent_is_known(self, reagent):
        if reagent in self._available_reagents:
            return
        self._err('Unknown reagent <%s>' % reagent)

    def _assert_units_are_known(self, units):
        if units in self._available_units:
            return
        self._err('Unknown units <%s>' % units)

    def _parse_column_spec(self, cols_spec):
        """
        Interprets (with error handling) strings like these, and returns
        a flat list of what they represent. (As integers).
            '1-12' or '3,4,5', or '3'
        """
        # Range?
        m = _INT_RANGE_RE.match(cols_spec)
        if m is not None:
            start, end = m.group(1,2)
            as_list = [str(x) for x in range(int(start), int(end)+1)]

        # Discrete list?
        elif ',' in cols_spec:
            as_list = cols_spec.split(',')

        # Must now be single value
        else:
            as_list = (cols_spec,)
        try:
            as_list = [int(s) for s in as_list]
        except ValueError:
            self._err('Problem with int() conversion in: <%s>' % cols_spec)
        return as_list

    def _parse_row_spec(self, rows_spec):
        """
        Interprets (with error handling) strings like these, and returns
        a flat list of what they represent. (As strings).
            'A-F' or 'A,B,C', or 'C'
        """
        # Range?
        m = _LETTER_RANGE_RE.match(rows_spec)
        if m is not None:
            start, end = m.group(1,2)
            as_list = [chr(x) for x in range(ord(start), ord(end)+1)]

        # Discrete list?
        elif ',' in rows_spec:
            as_list = rows_spec.split(',')

        # Must now be single value
        else:
            as_list = rows_spec,
        return as_list

    def _parse_conc_value(self, conc):
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
        return fields[0], fields

    def _err(self, message):
        message += ', at line number %d' % self._lnum
        raise ParseError(message)

_INT_RANGE_RE =re.compile(r'(\d+)-(\d+)$')
_LETTER_RANGE_RE =re.compile(r'([A-Z])-([A-Z])$')
