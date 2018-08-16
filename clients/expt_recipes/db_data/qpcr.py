from numpy.core.umath import isnan


_SPECIFIC_PRODUCT = '_spec'
_NON_SPECIFIC_PRODUCT = '_non_spec'
_PRIMER_DIMER = '_primer_dimer'


def create_payload(qdb_data, max_conc_mean_tm, mean_ntc_ct):
    tms = qdb_data['temperatures']
    tm_delta = [abs(tm - max_conc_mean_tm) if tm is not None else None for tm
                in tms ]
    ct =qdb_data['cycle_threshold']
    delta_ct = _calc_delta_ct(ct, mean_ntc_ct)
    ct_call = _get_ct_call(delta_ct)
    spec, non_spec, pd = _get_product_labels_from_tms(tms, tm_delta,
                                                      max_conc_mean_tm)
    return ct, delta_ct, ct_call, tms, spec, non_spec, pd


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


def _calc_delta_ct(ct, ntc_ct):
    """
    Calculate delta ct from a reference ntc value.
    :param ct: ct value
    :param ntc_ct: reference ntc value
    :return:
    """
    delta_ct = ntc_ct - ct if ct is not None else None
    return delta_ct


def _get_ct_call(delta_ct, ntc_ct_threshold=3.333333):
    """
    Get ct call given a delta ct and a relative ntc threshold ct value.
    :param delta_ct: a delta ct value
    :param ntc_ct_threshold: a relative ntc threshold ct value
    :return:
    """
    if delta_ct is None :
        return False
    if delta_ct > ntc_ct_threshold:
        return True
    else:
        return False


def _get_product_labels_from_tms(tms, tm_deltas, max_conc_mean_tm,
                                 tm_product_threshold=1,
                                 tm_primer_dimer_threshold=80):
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

    if _is_specific(tms[0], max_conc_mean_tm, tm_product_threshold):
        labels.add(_SPECIFIC_PRODUCT)

    for tm, tm_delta in zip(tms, tm_deltas):
        if _is_primer_dimer(tm, tm_delta, tm_product_threshold,
                            tm_primer_dimer_threshold):
            labels.add(_PRIMER_DIMER)
        if _is_non_specific(tm, tm_delta, tm_product_threshold,
                            tm_primer_dimer_threshold):
            labels.add(_NON_SPECIFIC_PRODUCT)

    spec = _SPECIFIC_PRODUCT in labels
    non_spec = _NON_SPECIFIC_PRODUCT in labels
    pd = _PRIMER_DIMER in labels

    return spec, non_spec, pd


def _is_specific(tm, max_conc_mean_tm, tm_product_threshold):
    """
    Determines whether a melting temperature is specific.
    :param tm: a melting temperature
    :param max_conc_mean_tm: average of the maximum template concentration wells
    :param tm_product_threshold: allowed threshold value
    :return:
    """
    if tm is None :
        return False
    if abs(tm - max_conc_mean_tm) < tm_product_threshold:
        return True
    else:
        return False


def _is_non_specific(tm: float, tm_delta: float, tm_product_threshold: float,
                     tm_primer_dimer_threshold: float):
    """
    Determines whether a melting temperature is non-specific.
    :param tm: a melting temperature
    :param tm_delta: a melting temperature delta calculated from a reference
    :param tm_product_threshold: melting temperature threshold value
    :param tm_primer_dimer_threshold: primer dimer threshold
    :return:
    """
    if tm is None :
        return False
    if tm > 0 and tm_delta > tm_product_threshold:
        if tm >= tm_primer_dimer_threshold:
            return True
        else:
            return False


def _is_primer_dimer(tm: float, tm_delta: float, tm_product_threshold: float,
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
    if tm is None :
        return False
    if tm > 0 and tm_delta > tm_product_threshold:
        if tm < tm_primer_dimer_threshold:
            return True
        else:
            return False
