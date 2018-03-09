from collections import OrderedDict
from app.rules_engine.alloc_rule import specific

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
        self._plates = [] # String identifiers.
        self._version = None

    def parse(self):
        """
        If the input is legitimate, runs to completion and returns results.
        Else raises ParseError.

        # The results structure is an ordered dict keyed on plate name.
        # The values are sequences of mixed AllocRule and TransferRule 
        # objects. 
        """
        results = OrderedDict()

        lines = self._script.splitlines()
        self._assert_version_in_first_line(lines)

        for i, line in lines:
            lnum = i + 1
            if self._comment_or_blank(line):
                continue
            first_field, all_fields = self._extract_fields(line)

            if first_field == 'P':
                self._known_plates.append(self._parse_plate_line(
                    fields, lnum))
            # Plate must be known for other types of lines to be legal.
            self._assert_a_plate_is_defined(lnum)
            if first_field == 'A':
                results[self._cur_plate()].append(
                    self._parse_A_line(fields, lnum))
            elif first_field == 'T':
                results[self._cur_plate()].append(
                    self._parse_T_line(fields, lnum))
            else:
                self._err('Line %d :Invalid rule type', lnum)
        return results

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _comment_or_blank(self, line):
        if line.isspace() or line.startswith('#'):
            return True

    def _parse_plate_line(self, fields, lnum):
        self._assert_there_are_n_fields(fields, 2, lnum)
        plate_name = fields[1]
        self._assert_plate_is_new(plate_name, lnum)
        return plate_name

    def _cur_plate(self):
        return self._plates[-1]

    def _parse_A_line(self, fields, lnum):
        self._assert_there_are_n_fields(fields, 6, lnum)
        _, reagent, cols, rows, conc, units = fields
        self._assert_reagent_is_known(reagent, lnum)
        cols = self._parse_column_spec(cols, lnum)
        rows = self._parse_row_spec(cols, lnum)
        conc_value = self._parse_conc_value(conc, lnum)
        conc_units = units
        self._assert_units_are_known(units, lnum)
        return AllocRule(reagent, cols, rows, conc, units)

    def _parse_T_line(self, fields, lnum):
        self._assert_there_are_n_fields(fields, 8, lnum)
        _, source_plate, s_cols, s_rows, d_cols, d_rows, conc, units = fields
        self._assert_plate_is_known(s_plate, lnum)
        self._assert_source_dest_compatibility(s_cols, s_rows, d_cols, d_rows)
        s_cols = self._parse_column_spec(s_cols, lnum)
        s_rows = self._parse_row_spec(s_cols, lnum)
        d_cols = self._parse_column_spec(d_cols, lnum)
        d_rows = self._parse_row_spec(d_cols, lnum)
        conc_value = self._parse_conc_value(conc, lnum)
        conc_units = units
        self._assert_units_is_dilution(conc_units, lnum)
        return TransferRule(source_plate, s_cols, s_rows, 
                d_cols, d_rows, conc, units)

    def _assert_version_in_first_line(self, lines):
        if len(lines) == 0:
            self._err('No lines present in input', lnum=0)
        first_field, all_fields = self._extract_fields(line)
        if first_field != 'V':
            self._err('Must have version in first line', lnum=0)
        version_string = all_fields[1]
        if version_string  != RulesScriptParser.VERSION:
            self._err(
                'This parser cannot handle version <%s> rules' % \
                version_string, lnum=0)

    def _assert_a_plate_is_defined(self, lnum):
        if len(self._plates) == 0:
            self._err('No plate is defined yet', lnum)

    def _assert_there_are_n_fields(self, fields, n, lnum):
        found = len(fields)
        if len(fields) != n:
            self._err('Should be %d fields, not %d' % (n, found), lnum)

    def _assert_plate_is_new(self, plate_name, lnum):
        if plate_name in self._plates:
            self._err('Plate name been used before (%s)' % plate_name, lnum)

    def _assert_reagent_is_known(self, reagent, lnum):
        if reagent in self._available_reagents:
            return
        self._err('Unknown reagent <%s>' % reagent, lnum)

    def _parse_column_spec(self, col_spec, lnum):
        resurrect prasanna's regexes here, using group harvesting
            

    def _extract_fields(self, line):
        """
        Separates the lines into fields and provides (as 2 returned values),
        the first field, and then all-fields.
        """
        fields = line.split()
        return fields[0], fields

    def _err(self, message, lnum)
        message += ' at line number %d' % lnum
        raise ParseError(message)
