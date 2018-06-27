
import numpy as np
from numpy.core.umath import isnan
from clients.expt_recipes.inst_data.data_models import IdQpcrData,IdQpcrMetaData


def make_nested_idqpcr_datas(well_constituents, qpcr_results):
    """
    Groups constituents by preamp assay and creates idqpcr data container for
    each well in group
    """
    id_qpcr_datas = {}
    max_conc_mean_tm = _calc_max_conc_mean_tm(well_constituents, qpcr_results)
    pa_grouped = _group_by_pa_assay(well_constituents)
    for pa_assay, pa_constits in pa_grouped.items():
        ntc_wells = _get_ntc_wells(pa_constits)
        qpcr_datas = [qpcr_results[w] for w in ntc_wells]
        mean_ntc_ct = default_ct_if_nan(get_mean_ct(qpcr_datas))
        for well in pa_constits:
            well_data = qpcr_results[well]
            idqpcr_data = IdQpcrData.create_from_db_data(well_data, max_conc_mean_tm,
                                               mean_ntc_ct)
            idqpcr_meta = IdQpcrMetaData.create_from_db_data(well_data)
            id_qpcr_datas[well] = {**idqpcr_data,**idqpcr_meta}


    return id_qpcr_datas


def make_vanilla_summary_idqpcr_datas(well_constituents, qpcr_results):
    """
    Creates Idqpcr data for each well present in well constituents
    """
    id_qpcr_datas = {}
    max_conc_mean_tm = _calc_max_conc_mean_tm(well_constituents,
                                    qpcr_results)
    ntc_wells = _get_ntc_wells(well_constituents)
    qpcr_datas = [qpcr_results[w] for w in ntc_wells]
    mean_ntc_ct = default_ct_if_nan(get_mean_ct(qpcr_datas))
    for well in well_constituents:
        well_data = qpcr_results[well]
        idqpcr_data = IdQpcrData.create_from_db_data(well_data,
                                                     max_conc_mean_tm,
                                                     mean_ntc_ct)
        idqpcr_meta = IdQpcrMetaData.create_from_db_data(well_data)
        id_qpcr_datas[well] = {**idqpcr_data,**idqpcr_meta}
    return id_qpcr_datas


# -----------------------------------------------------------------------
# Private below.
# -----------------------------------------------------------------------


def _calc_max_conc_mean_tm(id_qconsts, qinst_plate):
    """
    Calculates the melting temperature ("tm") for the wells that have
    the maximum concentration of template.

    For nested experiments, these are exclusively the id only template wells.

    :param id_qconsts: a dictionary of wells containing constituents
    :param qinst_plate: qPCR instrument data
    :return:
    """
    id_template_only_wells = _get_id_template_only_wells(id_qconsts)
    max_conc_wells = _get_max_conc_template_from_id_wells(id_template_only_wells)
    qpcr_datas = [qinst_plate[w] for w in max_conc_wells]
    max_conc_mean_tm = _calc_mean_tm(qpcr_datas)
    return max_conc_mean_tm

def _get_id_template_only_wells(id_qconsts):
    """
    Gets a dictionary of those wells which only contain template introduced
    at the id stage.

    :param id_qconsts: a dictionary of wells containing constituents
    :return:
    """
    id_template_only_wells = {}
    for well, contents in id_qconsts.items():
        if not 'transferred_templates' in contents and \
                'templates' in contents:
            id_template_only_wells[well] = contents
    return id_template_only_wells

def _get_max_conc_template_from_id_wells(id_qconsts):
    """
    Get from the id wells, those wells that have the highest template
    concentration.

    :param id_qconsts: a dictionary of wells containing constituents
    :return:
    """
    concs = dict((w, _get_item_attribute('templates',
                                              'concentration',wc))
                 for w, wc in id_qconsts.items())
    max_conc_wells = {}
    concentration_values = concs.values()
    if concentration_values:
        max_conc = max(concs.values())
        for w, c in id_qconsts.items():
            if concs[w] == max_conc:
                max_conc_wells[w] = c
    return max_conc_wells

def _get_item_attribute( key, attribute,contents):
    if key in contents:
        item = contents[key]
    else:
        item = []
    attributes = tuple(i[attribute] for i in item)
    return attributes

def _calc_mean_tm(qpcr_results,tm=0):
    temperatures = [result['temperatures'][tm] for result in qpcr_results]
    mean = np.mean(temperatures)
    return mean

def _get_ntc_wells(well_constituents):
    """
    Gets the ntc wells from a dictionary of WellConstituents
    :param well_constituents: dictionary of WellConstituents
    :return:
    """
    return dict(
        (w, wc) for w, wc in well_constituents.items() if _is_ntc(wc))

def _is_ntc(well_constituent):
    """
    Inspects a WellConstituent instance and determines whether it's an ntc.
    :param well_constituent: a WellConstituent
    :return:
    """
    templates = [v for k, v in well_constituent.items() if 'templates' in k]
    human = [v for k, v in well_constituent.items() if 'human' in k]
    return not any(templates + human)

def _group_by_pa_assay(id_qconsts):
    """
    Groups constituents by pa assay.
    :param id_qconsts: a dictionary of wells containing constituents
    :return:
    """
    wells_by_pa_assay = {}
    for w, wc in id_qconsts.items():
        pa_assay =_get_item_attribute('transferred_assays',
                                           'reagent_name', wc)

        inner = wells_by_pa_assay.setdefault(pa_assay, {})
        inner[w] = wc
    return wells_by_pa_assay

def get_mean_ct(qpcr_datas):
    """
    Gets the mean ct value from a dictionary of WellConstituents
    :param qpcr_datas: a list of qPCRInstWell instances
    :return:
    """
    cts = [qpcr['cycle_threshold'] for qpcr in qpcr_datas]
    cts = [ct for ct in cts if not ct is None]
    if cts:
        return np.mean(cts)
    else:
        return float('nan')

def default_ct_if_nan(ct, default= 40):
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
