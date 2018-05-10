from typing import Dict

from clients.expt_recipes.common.models import LabChipDatas, LabChipData
from clients.expt_recipes.nested.model_builders import Constituents
from clients.expt_recipes.well_constituents import WellConstituents
from hardware import labchip as hwlc
from hardware.plates import Plate, ExptPlates


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
    :return:
    """
    id_qpcr_constituents = {}
    for w, reagents in id_plate_reagents.items():
        id_qpcr_constituents[w] = \
            constituent_template.create(reagents, expt_plates)
    return id_qpcr_constituents


def build_labchip_datas_from_inst_data(
        id_qpcr_constituents: Constituents,
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
        lcw = mapping[idw]
        ass = constits.get_id_assay_attribute('reagent_name')
        lc_datas[idw] = \
            LabChipData.create_from_inst_data(lc_plate[lcw],
                                              [assays[a] for a in ass],
                                              dilutions[lcw])
    return lc_datas