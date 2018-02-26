import re
from collections import defaultdict


class ParseError(Exception):
    pass


class RuleScriptParser:
    """
    Class responsible for validating and parsing the rulescript text
    """

    _PARSES_LANGUAGE_VERSION = 1

    def __init__(self, reagents, units, script):
        self._available_reagents = reagents
        self._available_units = units
        self._script = script
        self._known_plates = []
        self._current_plate_no = None
        self._version = None
        self.result = defaultdict(dict)

    def parse(self):
        """
        If the input is legitimate, runs to completion.
        Else raises ParseError.
        :return: None
        """

        for i, line in enumerate(self._script.splitlines()):
            lnum = i + 1
            if lnum == 1:
                self._assert_version(line)
                continue
            if self._ignore_line(line):
                continue
            self.result[self._current_plate_no][lnum]={}
            line = line.strip()

            if line.startswith('P'):
                self._parse_plate_line(line, lnum)
            self._assert_plate_is_known(lnum)
            fields = self._extract_fields(line)
            field_type = fields[0]
            if field_type == 'A' or field_type == 'T':
                self._parse_rule_line(fields, lnum)
            else:
                ParseError('Line %d :Invalid rule type' % lnum)
        return self.result

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------
    _DIGIT_RANGE = re.compile(r'^\d+-\d+$')
    _DIGIT_SINGLE = re.compile(r'^\d+$')
    _DIGIT_COMMA = re.compile('^(?!,)(,?[0-9]+)+$')
    _LETTER_RANGE = re.compile('^[A-Z]-[A-Z]$')
    _LETTER_COMMA = re.compile('^(?!,)(,?[A-Z])+$')
    _LETTER_SINGLE = re.compile(r'^[A-Z]$')
    _PLATE_RULE = re.compile("^P\d+$")

    def _parse_plate_line(self, line, lnum):
        assert self._matches_one_of([self._PLATE_RULE], line, lnum), "Incorrect Plate Rule Pattern %d" % lnum
        field_type, plate_no = line
        self._current_plate_no = plate_no
        assert (plate_no not in self._known_plates), "Duplicate Plate rule %d" % lnum
        self._known_plates.append(line)

    def _parse_rule_line(self, fields, lnum):
        """
        validates elements in a identified rule , after validation the rule is saved in state .
        """
        if len(fields) != 6:
            raise ParseError('Must be exactly 6 fields (line number %d' % lnum)

        field_indices = range(1, 6)
        field_interpreter = (self._interpret_reagent, self._interpret_col_range,
                           self._interpret_row_range, self._interpret_conc, self._interpret_unit)
        for field_idx, validator in zip(field_indices, field_interpreter):
            if field_idx == 1:
                validator(fields, lnum)
            else:
                validator(fields[field_idx], lnum)

        # self.result[self._current_plate_no][lnum] = fields

    def _interpret_reagent(self, fields, lnum):
        """
        Validates reagents in a identified rule , validation differs for A rule and T rule
        """
        if fields[0] == 'A':
            if fields[1] in self._available_reagents:
                self.result[self._current_plate_no][lnum].setdefault('rule_type',fields[0])
                self.result[self._current_plate_no][lnum].setdefault('reagent', fields[1])
            else:
                raise ParseError('Line %d : Invalid reagent' % lnum)
        elif fields[0] == 'T':
            if fields[1] in self._known_plates:
                self.result[self._current_plate_no][lnum].setdefault('rule_type', fields[0])
                self.result[self._current_plate_no][lnum].setdefault('reagent', fields[1])
            else:
                raise ParseError('Line %d : Invalid reagent' % lnum)

    def _assert_plate_is_known(self, lnum):
        assert self._current_plate_no is not None, "Plate rule not found parsed %d lines" % lnum

    def _assert_version(self, line):
        fields = line.split()
        assert (line.startswith('V') and int(
            fields[1]) == self._PARSES_LANGUAGE_VERSION), "Invlid Version rule/No version rule"
        self._version = fields[1]

    def _ignore_line(self, line):
        if line.isspace() or line.strip().startswith('#'):
            return True

    def _extract_fields(self, line):
        fields = line.split()
        if len(fields) > 6:
            raise ParseError("Too Many fields to extract in : %s" % line)
        return fields

    def _matches_one_of(self, list_of_regex, string, lnum):
        for re in list_of_regex:
            if re.match(string):
                return True
        raise ParseError('Line %d : Not a valid row/col range ' % lnum)

    def _interpret_col_range(self, string, lnum):
        if self._matches_one_of([self._DIGIT_SINGLE, self._DIGIT_RANGE, self._DIGIT_COMMA], string, lnum):
                self.result[self._current_plate_no][lnum].setdefault('col_range', string)



    def _interpret_row_range(self, string, lnum):
        if self._matches_one_of([self._LETTER_SINGLE, self._LETTER_RANGE, self._LETTER_COMMA], string, lnum):
            self.result[self._current_plate_no][lnum].setdefault('row_range', string)

    def _interpret_conc(self, value, lnum):
        try:
            val = float(value)
            if val >= 0:
                self.result[self._current_plate_no][lnum].setdefault('conc', value)
            else:
                return False
        except ValueError:
            return ParseError('Line %d : Concentration not a float' % lnum)

    def _interpret_unit(self, value, lnum):
        if value in self._available_units:
            self.result[self._current_plate_no][lnum].setdefault('unit', value)
        else:
            return ParseError('Line %d : Given unit is not a part of recognised units' % lnum)
