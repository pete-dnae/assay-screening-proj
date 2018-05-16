from collections import OrderedDict

from clients.expt_recipes.interp.labchip import \
    get_product_label_from_peak_bp_concs
from clients.expt_recipes.interp.qpcr import calc_delta_ct, get_ct_call, \
    get_product_labels_from_tms
from hardware.labchip import extract_bp_conc_pairs
from hardware.qpcr import get_tms, calc_tm_deltas, get_ct


class IdQpcrData(OrderedDict):

    def __init__(self):
        super().__init__()
        self['Ct'] = None
        self['∆NTC Ct'] = None
        self['Ct Call'] = None
        self['Tm1'] = None
        self['Tm2'] = None
        self['Tm3'] = None
        self['Tm4'] = None
        self['Tm Specif'] = None
        self['Tm NS'] = None
        self['Tm PD'] = None

    @classmethod
    def create(cls, ct, delta_ct, ct_call, tms, spec, non_spec, pd):
        inst = cls()
        inst['Ct'] = ct
        inst['∆NTC Ct'] = delta_ct
        inst['Ct Call'] = ct_call
        inst['Tm1'] = tms[0]
        inst['Tm2'] = tms[1]
        inst['Tm3'] = tms[2]
        inst['Tm4'] = tms[3]
        inst['Tm Specif'] = spec
        inst['Tm NS'] = non_spec
        inst['Tm PD'] = pd
        return inst

    @classmethod
    def create_from_inst_data(cls, qinst_data, max_conc_mean_tm, mean_ntc_ct):

        tms = get_tms(qinst_data)
        tm_delta = calc_tm_deltas(qinst_data, max_conc_mean_tm)
        ct = get_ct(qinst_data)
        delta_ct = calc_delta_ct(ct, mean_ntc_ct)
        ct_call = get_ct_call(delta_ct)
        spec, non_spec, pd = get_product_labels_from_tms(tms, tm_delta,
                                                         max_conc_mean_tm)
        inst = cls()
        return inst.create(ct, delta_ct, ct_call, tms, spec, non_spec, pd)


class LabChipData(OrderedDict):

    def __init__(self):
        super().__init__()
        self['Specif ng/ul'] = None
        self['NS ng/ul'] = None
        self['PD ng/ul'] = None

    @classmethod
    def create(cls, spec, non_spec, pd):
        inst = cls()
        inst['Specif ng/ul'] = spec
        inst['NS ng/ul'] = non_spec
        inst['PD ng/ul'] = pd
        return inst

    @classmethod
    def create_from_inst_data(cls, linst_data, expected_amp_lens, dilution):
        bp_concs = extract_bp_conc_pairs(linst_data)
        spec, non_spec, pd = \
            get_product_label_from_peak_bp_concs(bp_concs,
                                                 expected_amp_lens,
                                                 dilution)
        inst = cls()
        return inst.create(spec, non_spec, pd)


def build_qpcr_constituents(qwell_reagents, constituent_template):
    """
    Builds a dictionary keyed by the well names. The values are instances of
    `IdConstituents`
    :param qwell_reagents: a dictionary keyed by well name and valued by
    instances of List[ObjReagent]
    :param constituent_template: The constituent template for the given well
    for a given experiment. For example a vanilla or nested constituents
    template.
    :return:
    """
    id_qpcr_constituents = {}
    for w, reagents in qwell_reagents.items():
        id_qpcr_constituents[w] = constituent_template.create(reagents)
    return id_qpcr_constituents


def build_labchip_datas_from_inst_data(id_qconsts, linst_plate, ql_mapping,
                                       assays, dilutions):
    """
    Build a dictionary of LabchipData instances keyed on their parent
    qPCR well.

    :param id_qconsts: a dictionary of id well constituents
    :param linst_plate: a dictionary of labchip instrument data
    :param ql_mapping: a dictionary that maps between qPCR and labchip wells
    :param assays: a dictionary that maps between an assay and it's expected
    amplicon length
    :param dilutions: a dictionary of labchip wells and their dilution factors
    :return:
    """
    lc_datas = {}
    for idw, constits in id_qconsts.items():
        # If a Labchip was run, populate an instance
        if idw in ql_mapping:
            lcw = ql_mapping[idw]
            ass = constits.get_id_assay_attribute('reagent_name')
            lc_datas[idw] = \
                LabChipData.create_from_inst_data(linst_plate[lcw],
                                                  [assays[a] for a in ass],
                                                  dilutions[lcw])
        else:
            # Or create an empty instance
            lc_datas[idw] = LabChipData()
    return lc_datas


def is_ntc(well_constituent):
    """
    Inspects a WellConstituent instance and determines whether it's an ntc.
    :param well_constituent: a WellConstituent
    :return:
    """
    templates = [v for k, v in well_constituent.items() if 'templates' in k]
    human = [v for k, v in well_constituent.items() if 'human' in k]
    return not any(templates + human)


def get_ntc_wells(well_constituents):
    """
    Gets the ntc wells from a dictionary of WellConstituents
    :param well_constituents: dictionary of WellConstituents
    :return:
    """
    return dict((w, wc) for w, wc in well_constituents.items() if is_ntc(wc))
