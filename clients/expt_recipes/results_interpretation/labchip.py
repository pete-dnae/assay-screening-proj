
import numpy as np
from hardware.labchip import get_peaks, get_peak_bp_size, get_peak_concentration


def is_specific(amplicon_lengths, bp, threshold=0.1):
    """function to find is a peak is specific ,In multiplex
     assays if amplicon length is within 10% of any of the
     target bp then its considered specific.Single plex if
     amplicon len is within 10% of targ bp then specific"""
    for amp in amplicon_lengths:
        error = np.abs((amp - bp) / amp)
        if error < threshold:
            return True
    return False


def is_primer_dimer(amplicon_length, primer_dimer_threshold=80):
    if amplicon_length < primer_dimer_threshold:
        return True
    else:
        return False


def get_product_label_from_labchip(labchip_data, amplicon_lengths, dilution,
                                   min_legal_length=10, max_legal_length=1400,
                                   pd_threshold=80):
    spec = 0
    pd = 0
    non_spec = 0

    peaks = get_peaks(labchip_data)
    for peak, peak_data in peaks.items():
        bp = get_peak_bp_size(peak_data)
        conc = get_peak_concentration(peak_data) * dilution
        if min_legal_length < bp < max_legal_length:
            if is_specific(amplicon_lengths, bp):
                spec += conc
            elif bp < pd_threshold:
                pd += conc
            else:
                non_spec += conc
    return spec, non_spec, pd
