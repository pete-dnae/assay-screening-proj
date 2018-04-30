
from typing import NewType, Dict, List, Union
from re import search

from clients.reagents import ObjReagent
from clients.reagents import cached_db_reagent_2_obj_reagent

WellName = NewType('WellName', str)
PlateName = NewType('PlateName', str)
Plate = Dict[WellName, List[ObjReagent]]
ExptPlates = Dict[PlateName, Plate]


def row_idx_to_plate_alpha(ridx: Union[str, int]) -> str:
    """
    Converts a numerical row index to an alpha value.
    :param ridx: row index to convert to alpha
    :return:
    """
    return chr(int(ridx)+64)


def row_col_to_well(ridx: Union[str, int], cidx: Union[str, int]) -> WellName:
    """
    Converts row and column indices to standard well names i.e. a single
    alpha followed by two numerals.
    :param ridx: row index to convert to alpha
    :param cidx: col index to convert to standard double numeral
    :return:
    """
    well_name = '{}{:0>2}'.format(row_idx_to_plate_alpha(ridx), cidx)
    return well_name


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


def create_plates_from_allocation_table(allocation_table) -> ExptPlates:
    """
    Creates a nested dictionary, indexed by plates and then wells. The values
    are reagent objects.
    :param allocation_table: the python object returned from calling
    `create_allocation_table`
    :return:
    """
    plates = {}
    reagent_cache = {}

    for pid, plate in allocation_table.items():
        plates[pid] = {}
        for cidx in plate:
            for ridx in plate[cidx]:
                w = row_col_to_well(ridx, cidx)
                reagents = []
                for r in plate[cidx][ridx]:
                    reagents.append(
                        cached_db_reagent_2_obj_reagent(r, reagent_cache))
                plates[pid][w] = reagents

    return plates
