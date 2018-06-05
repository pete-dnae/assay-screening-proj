from collections import OrderedDict
import re
from .utilities import well_position_to_numeric


def make_well_constituents(plate_id, wells, allocation_results,
                           reagent_categories):
    """
    Makes a well constituents dictionary for a mentioned plate and set of
    wells
    """
    well_constituents = {}
    for well_id in wells:

        transfered_reagents = _get_transfered_reagents(allocation_results,
                                                       reagent_categories,
                                                       plate_id ,well_id)
        source_reagents = _get_alocation_reagents(allocation_results,
                                                  reagent_categories,
                                                  plate_id,
                                                  well_id)
        transfered_reagents = \
            _get_transfer_reagents_package(transfered_reagents)
        reagents = _get_reagents_package(source_reagents)
        well_constituents[well_id] = {**transfered_reagents, **reagents}

    return well_constituents

def _get_transfer_reagents_package(reagents):
    """
    Creates a dictionary for transferred reagents , assumes reagents passed
    in are transfer reagents
    """
    well_constituent = {}
    for reagent in reagents:
        if reagent['reagent_category'] == 'assay':
            well_constituent.setdefault('transferred_assays',
                                        []).append(reagent)
        if reagent['reagent_category'] == 'template':
            well_constituent.setdefault('transferred_templates',
                                        []).append(reagent)
        if reagent['reagent_category'] == 'human':
            well_constituent.setdefault('transferred_humans',
                                        []).append(reagent)
    return well_constituent

def _get_reagents_package( reagents):
    """
       Creates a dictionary for  reagents , assumes reagents passed
       in are not transfer reagents
       """
    well_constituent = {}
    for reagent in reagents:
        if reagent['reagent_category'] == 'assay':
            well_constituent.setdefault('assays', []).append(reagent)

        if reagent['reagent_category'] == 'template':
            well_constituent.setdefault('templates', []).append(reagent)
        if reagent['reagent_category'] == 'human':
            well_constituent.setdefault('humans', []).append(reagent)
    return well_constituent



def _get_transfered_reagents(allocation_results, reagent_category, plate_id,
                             well_id):
    """
    Identifies and returns transfer reagents if any for a particular well in a
    plate
    """
    row, col = well_position_to_numeric(well_id)
    source_well = allocation_results.source_map[plate_id][col][row]

    if source_well:
        s_plate, s_row, s_col = _get_source_plate_row_col(source_well)

        well_allocation = allocation_results.plate_info[s_plate][s_col][s_row]
        return _get_reagents(well_allocation,reagent_category)
    else:
        return []

def _get_alocation_reagents(allocation_results, reagent_category, plate_id,
                            well_id):
    """
     Identifies and returns allocation reagents for a particular well in a plate
    """
    row, col = well_position_to_numeric(well_id)

    well_allocation = allocation_results.plate_info[plate_id][col][row]
    return _get_reagents(well_allocation,reagent_category)

def _get_reagents(well_allocation,reagent_category):
    """
    Helper function to get reagents of specific category in well allocation
    """
    results = []
    for (reagent, conc, unit) in well_allocation:
        if reagent in reagent_category:
            results.append({'concentration': conc,
                            'reagent_category': reagent_category[reagent],
                            'reagent_name': reagent,
                            'unit': unit})
    return results

def _get_source_plate_row_col(source_well):
    """
    function to split source well dictionary into a tuple
    """
    return source_well['source_plate'], source_well['source_row'], \
           source_well['source_col']

