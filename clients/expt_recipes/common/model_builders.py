
from clients.expt_recipes.well_constituents import WellConstituents
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