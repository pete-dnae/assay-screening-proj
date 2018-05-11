from typing import Dict

from clients.expt_recipes.common.models import WellConstituents
from clients.transfers import get_parent_wells, get_dilutions
from hardware.plates import Plate


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


def get_assay_amplicon_lengths():
    return None


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


def is_ntc(wc: WellConstituents) -> bool:
    """
    Inspects a WellConstituents instances and determines whether it's an ntc.
    :param wc: a WellConstituents instance
    :return:
    """
    templates = [v for k, v in wc.items() if 'templates' in k]
    human = [v for k, v in wc.items() if 'human' in k]
    return not any(templates + human)


def get_ntc_wells(wcs: Dict[str, WellConstituents])\
        -> Dict[str, WellConstituents]:
    """
    Gets the ntc wells from a dictionary of WellConstituents
    :param wcs: dictionary of WellConstituents
    :return:
    """
    return dict((w, wc) for w, wc in wcs.items() if is_ntc(wc))
