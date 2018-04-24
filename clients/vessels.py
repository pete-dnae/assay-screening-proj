from typing import NewType, Dict, List
from clients.reagents import Reagent

Contents = List[Reagent]
WellName = NewType('WellName', str)
Plates = Dict[WellName, Contents]


def row_idx_to_plate_alpha(ridx) -> str:
    return chr(int(ridx) +64)


def row_col_to_well(ridx, cidx) -> WellName:
    well = '{}{:0>2}'.format(row_idx_to_plate_alpha(ridx), cidx)
    return well
