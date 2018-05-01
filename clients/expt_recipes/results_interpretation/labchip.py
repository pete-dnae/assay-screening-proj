
import numpy as np

def is_specific(amplicon_length, bp, specific_hreshold):
    """function to find is a peak is specific ,In multiplex
     assays if amplicon length is within 10% of any of the
     target bp then its considered specific.Single plex if
     amplicon len is within 10% of targ bp then specific"""
    for bp_len in amplicon_length.values():
        error = np.abs((bp_len - bp) / bp_len)
        if error < specific_hreshold:
            return True
    return False


def is_primer_dimer(amplicon_length, primer_dimer_threshold=80):
    if amplicon_length < primer_dimer_threshold:
        return True
    else:
        return False


def calc_smth(lc_peak_data, dilution, max_legal_length=1400,
              min_legal_length=10, specific_peak_threshold=0.1,
              primer_dimer_length_threshold=80):

    specific_purity = 0
    specific_conc = 0
    primer_dimer_purity = 0
    primer_dimer_conc = 0
    non_specific_purity = 0
    non_specific_conc = 0

    for peak, data in lc_peak_data.items():
        bp = data['size_[bp]']
        purity = data['%_purity']
        conc = get_concentration(data, dilution)
        # With the help of threshold limits find weather a sample is Specific,Non Specific or PD
        if bp != '' and min_legal_length < bp < max_legal_length:
            is_specific = _isspecific(assays, bp, specific_peak_threshold)
            is_primerdimer = (bp < primer_dimer_length_threshold)
            if is_specific and purity > specific_purity:
                specific_purity += purity
                specific_conc += conc
            elif is_primerdimer:
                primer_dimer_purity += purity
                primer_dimer_conc += conc
            else:
                non_specific_purity += purity
                non_specific_conc += conc
