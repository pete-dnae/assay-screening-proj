from re import search
from typing import NewType

WellName = NewType('WellName', str)


def sanitize_well_name(well_name: str) -> WellName:
    """
    Sanitize non-standard well names to a standard nomenclature.
    :param well_name: a potentially non-standard well name i.e. a single alpha
    followed by a SINGLE numeral
    :return:
    """
    searched = search('([a-zA-Z]+)(\d+)', well_name).groups()
    well_name = '{}{:0>2}'.format(searched[0], searched[1])
    return well_name
