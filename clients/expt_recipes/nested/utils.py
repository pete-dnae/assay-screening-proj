from typing import List, Dict

import re

from clients.transfers import get_parent_wells, get_dilutions
from hardware.plates import ExptPlates, Plate


def get_id_qpcr_plate_names(all_expt_plates: ExptPlates) -> List[str]:
    """
    Extracts those plates in a nested experiment which are the id plates.
    :param all_expt_plates: all plates used for an experiment
    :return:
    """
    id_plate_names = [p for p in all_expt_plates if p.endswith('_ID')]
    if not id_plate_names:
        raise ValueError('No id plates detected.')
    else:
        return id_plate_names


def get_labchip_plate_names(all_expt_plates: ExptPlates) -> List[str]:
    """
    Extracts those plates in a nested experiment which are the labchip plates.
    :param all_expt_plates: all plates used for an experiment
    :return:
    """
    lc_plate_names = []
    for p in all_expt_plates:
        searched = re.search('\d{8}_\w', p)
        if searched:
            lc_plate_names.append(searched.group())
    if not lc_plate_names:
        raise ValueError('No LabChip plates detected!')
    else:
        return lc_plate_names


def create_id_qpcr_lc_mapping(lc_plate: Plate) -> Dict[str, str]:
    """
    Creates a dictionary between a qpcr well and a child labchip well.
    :param lc_plate: a labchip `Plate` instance
    :return:
    """
    id_qpcr_lc_mapping = {}
    for lcw, reagents in lc_plate.items():
        parents = get_parent_wells(reagents)
        if len(parents) > 1:
            raise ValueError('Labchip well {} has more than one parent '
                             'qpcr well'.format(lcw))
        _, idw = parents[0]
        id_qpcr_lc_mapping[idw] = lcw
    return id_qpcr_lc_mapping


def get_lc_dilutions(lc_plate: Plate) -> Dict[str, float]:
    """
    Get the dilution factors for each labchip well.
    :param lc_plate: a labchip `Plate` instance
    :return:
    """
    lc_dilutions = {}
    for w, reagents in lc_plate.items():
        dilutions = get_dilutions(reagents)
        if len(dilutions) > 1:
            raise ValueError('Labchip well {} has more than one parent '
                             'qpcr well'.format(w))
        lc_dilutions[w] = dilutions[0]
    return lc_dilutions
