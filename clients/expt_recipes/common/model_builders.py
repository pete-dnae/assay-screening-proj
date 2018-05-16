from typing import Dict

from clients.expt_recipes.common.utils import get_ntc_wells
from clients.expt_recipes.common.models import WellConstituents, \
    ConstituentsByWell, LabChipDatas, LabChipData
from hardware import qpcr as hwq, labchip as hwlc
from clients.expt_recipes.interp.db_query import Plate, ExptPlates


def build_id_qpcr_constituents(
        id_plate_reagents: Plate,
        expt_plates: ExptPlates,
        constituent_template: WellConstituents):
    """
    Builds a dictionary keyed by the well names. The values are instances of
    `IdConstituents`
    :param id_plate_reagents: a dictionary keyed by well name and valued by
    instances of List[ObjReagent]
    :param expt_plates: an instance of ExptPlates for this particular
    experiment
    :param constituent_template: The constituent template for the given well
    for a given experiment. For example a vanilla or nested constituents
    template.
    :return:
    """
    id_qpcr_constituents = {}
    for w, reagents in id_plate_reagents.items():
        id_qpcr_constituents[w] = \
            constituent_template.create(reagents, expt_plates)
    return id_qpcr_constituents


def calc_mean_ntc_ct(constituents: ConstituentsByWell,
                     raw_instrument_data: hwq.qPCRInstPlate) -> float:
    """

    :param constituents: a dictionary keyed by well name and valued by
    instances of `IdConstituents`
    :param raw_instrument_data: qPCR instrument data
    :return:
    """
    ntc_wells = get_ntc_wells(constituents)
    qpcr_datas = [raw_instrument_data[w] for w in ntc_wells]
    mean_ntc_ct = hwq.get_mean_ct(qpcr_datas)
    return mean_ntc_ct


def build_labchip_datas_from_inst_data(
        id_qpcr_constituents: ConstituentsByWell,
        lc_plate: hwlc.LabChipInstPlate,
        mapping: Dict[str, str],
        assays: Dict[str, int],
        dilutions: Dict[str, float]) -> LabChipDatas:
    """
    Build a dictioanry of `NestedLabchipData` instances keyed on their parent
    qPCR well.

    :param id_qpcr_constituents: a dictionary keyed by well name and valued by
    instances of `IdConstituents`
    :param lc_plate: the Labchip instrument data
    :param mapping: a dictioanry that maps between qPCR and labchip wells
    :param assays: a dictionary that maps between an assay and it's expected
    amplicon length
    :param dilutions: a dictionary of labchip wells and their dilution factors
    :return:
    """
    lc_datas = {}
    for idw, constits in id_qpcr_constituents.items():
        # If a Labchip was run, populate an instance
        if idw in mapping:
            lcw = mapping[idw]
            ass = constits.get_id_assay_attribute('reagent_name')
            lc_datas[idw] = \
                LabChipData.create_from_inst_data(lc_plate[lcw],
                                                  [assays[a] for a in ass],
                                                  dilutions[lcw])
        else:
            # Or create an empty instance
            lc_datas[idw] = LabChipData()
    return lc_datas