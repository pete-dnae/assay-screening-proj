
from typing import NewType, Dict, List
from re import search

from clients.reagents import Reagent
from clients.reagents import cached_reformat_db_reagent

Contents = List[Reagent]
WellName = NewType('WellName', str)
PlateName = NewType('PlateName', str)
Plates = Dict[PlateName, Dict[WellName, Contents]]


def row_idx_to_plate_alpha(ridx) -> str:
    return chr(int(ridx)+64)


def row_col_to_well(ridx, cidx) -> WellName:
    well = '{}{:0>2}'.format(row_idx_to_plate_alpha(ridx), cidx)
    return well


def sanitize_well_name(well_name) -> WellName :
    searched = search('([a-zA-Z]+)(\d+)', well_name).groups()
    well_name = '{}{:0>2}'.format(searched[0], searched[1])
    return well_name


def create_plates_from_expt(allocation_table) -> Plates:

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
                        cached_reformat_db_reagent(r, reagent_cache))
                plates[pid][w] = reagents

    return plates
