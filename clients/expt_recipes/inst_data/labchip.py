import numpy as np

from hardware.labchip import extract_bp_conc_pairs


def create_payload(linst_data, expected_amp_lens, dilution):
    bp_concs = extract_bp_conc_pairs(linst_data)
    spec, non_spec, pd = \
        _get_product_label_from_peak_bp_concs(bp_concs,
                                              expected_amp_lens,
                                              dilution)
    return spec, non_spec, pd


def _get_product_label_from_peak_bp_concs(bp_concs, amplicon_lengths, dilution,
                                          min_legal_length=10,
                                          max_legal_length=1400,
                                          pd_threshold=80):
    spec = 0
    pd = 0
    non_spec = 0

    for bp_conc in bp_concs:
        bp, conc = bp_conc[0], bp_conc[1] * dilution
        if min_legal_length < bp < max_legal_length:
            if _is_specific(amplicon_lengths, bp):
                spec += conc
            elif bp < pd_threshold:
                pd += conc
            else:
                non_spec += conc
    return spec, non_spec, pd


def _is_specific(amplicon_lengths, bp, threshold=0.1):

    for amp in amplicon_lengths:
        error = np.abs((amp - bp) / amp)
        if error < threshold:
            return True
    return False


def _is_primer_dimer(amplicon_length, primer_dimer_threshold=80):
    if amplicon_length < primer_dimer_threshold:
        return True
    else:
        return False
