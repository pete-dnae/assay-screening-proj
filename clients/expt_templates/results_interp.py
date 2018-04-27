
from typing import List
import numpy as np

from clients.expt_templates.well_constituents import WellConstituents

SPECIFIC_PRODUCT = '_spec'
NON_SPECIFIC_PRODUCT = '_non_spec'
PRIMER_DIMER = '_primer_dimer'


def get_ct(qpcr_data):
    ct = qpcr_data['results']['results']['ct']
    if ct:
        return ct
    else:
        return np.nan


def get_tm(qpcr_data, tm):
    tm = qpcr_data['results']['results'][tm]
    if tm:
        return tm
    else:
        return np.nan


def get_tms(qpcr_data, tms=('tm1', 'tm2', 'tm3', 'tm4')):
    tms = [get_tm(qpcr_data, tm) for tm in tms]
    return tms


def is_ntc(wc: WellConstituents):
    templates = [v for k, v in wc.items() if 'templates' in k]
    human = [v for k, v in wc.items() if 'human' in k]
    return not any(templates + human)


def get_ntc_wells(well_contents: List[WellConstituents]):
    return [wc for wc in well_contents if is_ntc(wc)]


def get_mean_ct(well_contents: List[WellConstituents],
                plate_data,
                excl_nans=True):
    wells = [wc['well_name'] for wc in well_contents]
    cts = [get_ct(plate_data[w]) for w in wells]
    if excl_nans:
        return np.nanmean(cts)
    else:
        return np.mean(cts)


def get_delta_ct(ct, ntc_ct):
    delta_ct = ntc_ct - ct
    return delta_ct


def get_ct_call(delta_ct, ntc_ct_threshold=1/3):
    if delta_ct > ntc_ct_threshold:
        return 'POS'
    else:
        return 'NEG'


def calc_mean_tm(well_contents: List[WellConstituents],
                 plate_data,
                 tm='tm1'):
    wells = [wc['well_name'] for wc in well_contents]
    mean_tm = np.mean([get_tm(plate_data[w], tm) for w in wells])
    return mean_tm


def get_tm_delta(qpcr_data, max_conc_mean_tm):
    tms = get_tms(qpcr_data)
    tm_delta = [abs(tm - max_conc_mean_tm) for tm in tms]
    return tm_delta


def is_specific(tm, max_conc_mean_tm, tm_product_threshold):
    if abs(tm - max_conc_mean_tm) < tm_product_threshold:
        return True
    else:
        return False


def is_non_specific(tm, tm_delta, tm_product_threshold,
                    tm_primer_dimer_threshold):
    if tm > 0 and tm_delta > tm_product_threshold:
        if tm >= tm_primer_dimer_threshold:
            return True
        else:
            return False


def is_primer_dimer(tm, tm_delta, tm_product_threshold,
                    tm_primer_dimer_threshold):
    if tm > 0 and tm_delta > tm_product_threshold:
        if tm < tm_primer_dimer_threshold:
            return True
        else:
            return False


def get_product_labels_from_tms(tms, tm_deltas,
                                max_conc_mean_tm,
                                tm_product_threshold=1,
                                tm_primer_dimer_threshold=80):
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

    return labels
