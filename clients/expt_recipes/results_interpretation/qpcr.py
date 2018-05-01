from typing import List, Dict

import numpy as np

from hardware.plates import WellName
from hardware.qpcr import qPCRData, get_ct, get_tm

SPECIFIC_PRODUCT = '_spec'
NON_SPECIFIC_PRODUCT = '_non_spec'
PRIMER_DIMER = '_primer_dimer'


def get_mean_ct(well_names: List[str],
                plate_data: Dict[WellName, qPCRData]):
    """
    Gets the mean ct value from a dictionary of WellConstituents
    :param well_names: well names to average across
    :param plate_data: a dictionary of `qPCRData` instances
    :return:
    """
    cts = [get_ct(plate_data[w]) for w in well_names]
    cts = [ct for ct in cts if not np.isnan(ct)]
    if cts:
        return np.mean(cts)
    else:
        return np.nan


def calc_delta_ct(ct: float, ntc_ct: float) -> float:
    """
    Calculate delta ct from a reference ntc value.
    :param ct: ct value
    :param ntc_ct: reference ntc value
    :return:
    """
    delta_ct = ntc_ct - ct
    return delta_ct


def get_ct_call(delta_ct: float, ntc_ct_threshold: float=1/3) -> str:
    """
    Get ct call given a delta ct and a relative ntc threshold ct value.
    :param delta_ct: a delta ct value
    :param ntc_ct_threshold: a relative ntc threshold ct value
    :return:
    """
    if delta_ct > ntc_ct_threshold:
        return 'POS'
    else:
        return 'NEG'


def calc_mean_tm(well_names: List[str],
                 plate_data: Dict[WellName, qPCRData],
                 tm='tm1'):
    """
    Calculate the mean tm for a set of wells and a particular tm value.
    :param well_names: well names to average across
    :param plate_data: a dictionary `qPCRData` instances
    :param tm: a dictionary `qPCRData` instances
    :return:
    """
    mean_tm = np.mean([get_tm(plate_data[w], tm)
                       for w in well_names])
    return mean_tm


def is_specific(tm: float, max_conc_mean_tm: float,
                tm_product_threshold: float) -> bool:
    """
    Determines whether a melting temperature is specific.
    :param tm: a melting temperature
    :param max_conc_mean_tm: average of the maximum template concentration wells
    :param tm_product_threshold: allowed threshold value
    :return:
    """
    if abs(tm - max_conc_mean_tm) < tm_product_threshold:
        return True
    else:
        return False


def is_non_specific(tm: float, tm_delta: float, tm_product_threshold: float,
                    tm_primer_dimer_threshold: float):
    """
    Determines whether a melting temperature is non-specific.
    :param tm: a melting temperature
    :param tm_delta: a melting temperature delta calculated from a reference
    :param tm_product_threshold: melting temperature threshold value
    :param tm_primer_dimer_threshold: primer dimer threshold
    :return:
    """
    if tm > 0 and tm_delta > tm_product_threshold:
        if tm >= tm_primer_dimer_threshold:
            return True
        else:
            return False


def is_primer_dimer(tm: float, tm_delta: float, tm_product_threshold: float,
                    tm_primer_dimer_threshold: float):
    """
    Determines whether a melting temperature is a primer dimer.

    :param tm: a melting temperature
    :param tm_delta: a melting temperature delta calculated from a reference
    melting temperature threshold value
    :param tm_product_threshold: melting temperature threshold value
    :param tm_primer_dimer_threshold: primer dimer threshold
    :return:
    """
    if tm > 0 and tm_delta > tm_product_threshold:
        if tm < tm_primer_dimer_threshold:
            return True
        else:
            return False


def get_product_labels_from_tms(tms: List[float], tm_deltas: List[float],
                                max_conc_mean_tm: float,
                                tm_product_threshold: float=1,
                                tm_primer_dimer_threshold: float=80):
    """
    Get a tuple of booleans indicating if a set of melting temperatures
    is one of, or a combination thereof of the following:
    specific, non-specific or primer dimer.

    :param tms: melting temperatures
    :param tm_deltas: melting temperature deltas calculated from a reference
    :param max_conc_mean_tm: average of the maximum template concentration wells
    :param tm_product_threshold: melting temperature threshold value
    :param tm_primer_dimer_threshold: primer dimer threshold
    :return:
    """
    labels = set()

    if is_specific(tms[0], max_conc_mean_tm, tm_product_threshold):
        labels.add(SPECIFIC_PRODUCT)

    for tm, tm_delta in zip(tms, tm_deltas):
        if is_primer_dimer(tm, tm_delta, tm_product_threshold,
                           tm_primer_dimer_threshold):
            labels.add(PRIMER_DIMER)
        if is_non_specific(tm, tm_delta, tm_product_threshold,
                           tm_primer_dimer_threshold):
            labels.add(NON_SPECIFIC_PRODUCT)

    spec = SPECIFIC_PRODUCT in labels
    non_spec = NON_SPECIFIC_PRODUCT in labels
    pd = PRIMER_DIMER in labels

    return spec, non_spec, pd
