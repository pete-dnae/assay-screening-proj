
from typing import Dict

from clients.expt_recipes.common.models import WellConstituents


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
