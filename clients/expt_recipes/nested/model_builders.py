
from clients.expt_recipes.nested.constituents import IdConstituents
from clients.expt_recipes.inst_data.qpcr import default_ct_if_nan
from clients.expt_recipes.inst_data.data_models import IdQpcrData
from clients.expt_recipes.lost import get_ntc_wells
# todo: this import needs to be removed (maybe the above too)
from hardware.qpcr import get_mean_ct, calc_mean_tm


def build_qpcr_constituents(qwell_reagents, all_expt_plates):
    """
    Builds a dictionary keyed by the well names. The values are instances of
    `IdConstituents`
    :param qwell_reagents: a dictionary keyed by well name and valued by
    instances of List[ObjReagent]
    :param all_expt_plates: a dictioanry containing all the allocations for
    all wells for all plates used in the experiment
    :return:
    """
    id_qpcr_constituents = {}
    for w, reagents in qwell_reagents.items():
        id_qpcr_constituents[w] = IdConstituents.create(reagents,
                                                        all_expt_plates)
    return id_qpcr_constituents


def build_id_qpcr_datas_from_inst_data(id_qconsts, qinst_data):
    """
    Creates a dictionary keyed by well names and valued by instances of
    `IdQpcrData`.

    Iterates over all the wells in a plates and initially groups them by the
    id assay and then the preamp assay. At various stages in the grouping
    process, intermediate values are calculated as they are required when
    creating a `IdQpcrData`.

    :param id_qconsts: a dictionary of wells containing constituents
    :param qinst_data: a dictionary of wells containing instrument data
    :return:
    """
    id_qpcr_datas = {}
    id_grouped = _group_by_id_assay(id_qconsts)
    for id_assay, id_constits in id_grouped.items():
        max_conc_mean_tm = \
            _calc_max_conc_mean_tm(id_constits, qinst_data)
        pa_grouped = _group_by_pa_assay(id_constits)
        for pa_assay, pa_constits in pa_grouped.items():
            ntc_wells = get_ntc_wells(pa_constits)
            qpcr_datas = [qinst_data[w] for w in ntc_wells]
            mean_ntc_ct = default_ct_if_nan(get_mean_ct(qpcr_datas))
            for w in pa_constits:
                well_data = qinst_data[w]
                id_qpcr_datas[w] = \
                    IdQpcrData.create_from_inst_data(well_data,
                                                     max_conc_mean_tm,
                                                     mean_ntc_ct)
    return id_qpcr_datas


def get_wells_by_id_assay(id_qconsts):
    """
    Creates a dictionary keyed by id assay and valued by associated well names.
    :param id_qconsts: a dictionary of wells containing constituents
    :return:
    """
    groupings = _create_nested_groupings(id_qconsts)

    wells_by_id_assay = {}
    for id_assay in groupings:
        wells_by_id_assay[id_assay] = []
        for pa_assay in groupings[id_assay]:
            for template in groupings[id_assay][pa_assay]:
                wells_by_id_assay[id_assay] = \
                    wells_by_id_assay[id_assay] + list(
                        groupings[id_assay][pa_assay][template].keys())
    return wells_by_id_assay


def _create_nested_groupings(id_qconsts):
    """
    Group nested wells based upon their constituents.
    :param id_qconsts: a dictionary of wells containing constituents
    :return:
    """
    groups = {}
    idgrp = _group_by_id_assay(id_qconsts)
    for id_assay, id_constits in idgrp.items():
        groups[id_assay] = {}
        pagrp = _group_by_pa_assay(id_constits)
        for pa_assay, pa_constits in pagrp.items():
            groups[id_assay][pa_assay] = {}
            tgrp = _group_by_template_origin(pa_constits)
            for t, t_constituents in tgrp.items():
                groups[id_assay][pa_assay][t] = t_constituents
    return groups


def _group_by_id_assay(id_qconsts):
    """
    Groups constituents by id assay.
    :param id_qconsts: a dictionary of wells containing constituents
    :return:
    """
    wells_by_id_assay = {}
    for w, c in id_qconsts.items():
        id_assay = c.get_id_assay_attribute('reagent_name')
        inner = wells_by_id_assay.setdefault(id_assay, {})
        inner[w] = c
    return wells_by_id_assay


def _group_by_pa_assay(id_qconsts):
    """
    Groups constituents by pa assay.
    :param id_qconsts: a dictionary of wells containing constituents
    :return:
    """
    wells_by_pa_assay = {}
    for w, c in id_qconsts.items():
        pa_assay = c.get_pa_assay_attribute('reagent_name')
        inner = wells_by_pa_assay.setdefault(pa_assay, {})
        inner[w] = c
    return wells_by_pa_assay


def _group_by_template_origin(id_qconsts):
    """
    Groups constituents by template origin.
    :param id_qconsts: a dictionary of wells containing constituents
    :return:
    """
    wells_by_template = {}
    for w, c in id_qconsts.items():
        pa_template = c.get_pa_template_attribute('reagent_name')
        id_template = c.get_id_template_attribute('reagent_name')
        if pa_template and not id_template:
            inner = wells_by_template.setdefault('preamp', {})
        elif id_template and not pa_template:
            inner = wells_by_template.setdefault('id', {})
        else:
            inner = wells_by_template.setdefault('NTC', {})
        inner[w] = c
    return wells_by_template


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
    max_conc_wells = \
        _get_max_conc_template_from_id_wells(id_template_only_wells)
    qpcr_datas = [qinst_plate[w] for w in max_conc_wells]
    max_conc_mean_tm = calc_mean_tm(qpcr_datas)
    return max_conc_mean_tm


def _get_id_template_only_wells(id_qconsts):
    """
    Gets a dictionary of those wells which only contain template introduced
    at the id stage.

    :param id_qconsts: a dictionary of wells containing constituents
    :return:
    """
    id_template_only_wells = {}
    for w, c in id_qconsts.items():
        if not c.get_pa_template_attribute('reagent_name') and \
                c.get_id_template_attribute('reagent_name'):
            id_template_only_wells[w] = c
    return id_template_only_wells


def _get_max_conc_template_from_id_wells(id_qconsts):
    """
    Get from the id wells, those wells that have the highest template
    concentration.

    :param id_qconsts: a dictionary of wells containing constituents
    :return:
    """
    concs = dict((w, wc.get_id_template_attribute('concentration'))
                 for w, wc in id_qconsts.items())
    max_conc = max(concs.values())

    max_conc_wells = {}
    for w, c in id_qconsts.items():
        if concs[w] == max_conc:
            max_conc_wells[w] = c
    return max_conc_wells
