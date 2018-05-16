from typing import List

import re

from clients.expt_recipes.interp.db_query import ExptPlates


def get_id_qpcr_plate_names(expt_plates: ExptPlates) -> List[str]:
    """
    Extracts those plates in a nested experiment which are the id plates.
    :param expt_plates: all plates used for an experiment
    :return:
    """
    lc_plate_names = get_labchip_plate_names(expt_plates)
    id_plate_names = list(set(expt_plates.keys) - set(lc_plate_names))
    if not id_plate_names:
        raise ValueError('No id plates detected.')
    else:
        return id_plate_names


def get_labchip_plate_names(expt_plates: ExptPlates) -> List[str]:
    """
    Extracts those plates in a nested experiment which are the labchip plates.
    :param expt_plates: all plates used for an experiment
    :return:
    """
    lc_plate_names = []
    for p in expt_plates:
        searched = re.search('\d{8}_\w', p)
        if searched:
            lc_plate_names.append(searched.group())
    if not lc_plate_names:
        raise ValueError('No LabChip plates detected!')
    else:
        return lc_plate_names