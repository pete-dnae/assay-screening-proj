
from typing import List
from numpy import isnan

SPECIFIC_PRODUCT = '_spec'
NON_SPECIFIC_PRODUCT = '_non_spec'
PRIMER_DIMER = '_primer_dimer'


def default_ct_if_nan(ct: float, default: float=40):
    """
    Converts a unknown (i.e. nan) ct value to an appropriate default.
    :param ct: ct value to inspect
    :param default: default value to replace a nan
    :return:
    """
    if isnan(ct):
        return default
    else:
        return ct


def calc_delta_ct(ct: float, ntc_ct: float) -> float:
    """
    Calculate delta ct from a reference ntc value.
    :param ct: ct value
    :param ntc_ct: reference ntc value
    :return:
    """
    delta_ct = ntc_ct - ct
    return delta_ct


def get_ct_call(delta_ct: float, ntc_ct_threshold: float=1/3) -> bool:
    """
    Get ct call given a delta ct and a relative ntc threshold ct value.
    :param delta_ct: a delta ct value
    :param ntc_ct_threshold: a relative ntc threshold ct value
    :return:
    """
    if delta_ct > ntc_ct_threshold:
        return True
    else:
        return False


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
