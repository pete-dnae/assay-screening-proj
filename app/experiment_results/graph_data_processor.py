from scipy.stats import linregress
import numpy as np
from .experiment_data_extractor import get_qpcr_results_by_well,\
    get_labchip_results_from_queryset,get_dilutions


def prepare_amp_graph(well_constituents,qpcr_queryset):
    qpcr_data =get_qpcr_results_by_well(qpcr_queryset)
    amp_data = []

    for well_id,constituents in well_constituents.items():
        constituents['well_id']=well_id
        amp_data.append({
            'x':qpcr_data[well_id]['amplification_cycle'],
            'y':qpcr_data[well_id]['amplification_delta_rn'],
            'meta':constituents
        })

    return amp_data

def prepare_melt_graph(well_constituents,qpcr_queryset):
    qpcr_data = get_qpcr_results_by_well(qpcr_queryset)
    melt_data = []
    for well_id, constituents in well_constituents.items():
        constituents['well_id'] = well_id
        melt_data.append({
            'x': qpcr_data[well_id]['melt_temperature'],
            'y': qpcr_data[well_id]['melt_derivative'],
            'meta': constituents
        })
    return melt_data
def prepare_copy_count_graph(well_constituents, qpcr_queryset):
    try:
        qpcr_data = get_qpcr_results_by_well(qpcr_queryset)
        template, ct = _get_conc_ct_values(well_constituents,qpcr_data)
        eff, r2 = calc_eff_r2(template, ct)
        template = np.log10(template)
        x_for_fit = np.array(template, dtype=np.float32)
        a = np.vstack([x_for_fit, np.ones(len(x_for_fit))]).T
        y_for_fit = np.array(ct, dtype=np.float32)
        fit, residuals = np.linalg.lstsq(a, y_for_fit)[:2]
        slope, intercept = fit
        fitted_y = slope * x_for_fit + intercept
        return {'x1': x_for_fit.tolist(), 'y1': y_for_fit.tolist(),
             'y2': fitted_y.tolist(), 'r2': int(r2 * 100),
             'eff': 'nan' if np.isnan(eff) or np.isinf(eff) else eff}
    except:
        return {'x1': [], 'y1': [],'y2': [], 'r2': 'nan','eff': 'nan'}


def _get_conc_ct_values(well_constituents,qpcr_data):
    template_conc = []
    ct_vals = []
    for well_id,constituents in well_constituents.items():
        if 'templates' in constituents:
            template_conc.append(_get_concentration(constituents[
                                                             'templates']))
            ct_vals.append(_get_ct_value(well_id,qpcr_data))

    return template_conc,ct_vals

def _get_ct_value(well_id,qpcr_data):
    ct =qpcr_data[well_id]['cycle_threshold']
    if ct is None:
        return 40
    return ct

def _get_concentration(constituents):

    if len(constituents) >0 :
        return constituents[0]['concentration']
    else:
        return None

def calc_eff_r2(template, ct):
    """
    Function to calculate efficiency and r2
    :param template:
    :param ct:
    :return:
    """
    log_template = np.log10(template)
    if any(np.isinf(log_template)):
        raise ValueError("Can't calculate efficeincy with 'inf' values. "
                         "Have you removed NTCs?")
    lin_fit = linregress(log_template, ct)
    eff = (10 ** (-1 / lin_fit.slope) - 1)
    r2 = lin_fit.rvalue ** 2

    return eff, r2

def prepare_labchip_graph(well_constituents,labchip_query):
    """
    Includes dilution calculations and meta data about qpcr allocation to
    labchip results
    """

    labchip_qpcr_well_map = {record.labchip_well: record.qpcr_well.qpcr_well for record in
         labchip_query}
    labchip_results = get_labchip_results_from_queryset(labchip_query)
    dilutions = get_dilutions(labchip_query)
    for well_id,record in labchip_results.items():
        peak_data = record['peak']
        for key,peak in peak_data.items():
            peak['meta'] = well_constituents[labchip_qpcr_well_map[well_id]]
            peak['conc_(ng/ul)'] = peak['conc_(ng/ul)']*dilutions[well_id]
            peak_data[key] = peak
        labchip_results[well_id] = record
    return labchip_results


