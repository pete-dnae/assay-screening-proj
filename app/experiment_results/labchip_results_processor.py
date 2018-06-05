from hardware.labchip_peak import LabChipPeakProcessor

import math
from .utilities import well_position_to_numeric,\
    well_position_to_alpha_numeric,fetch_wells
from .experiment_data_extractor import fetch_qpcr_well,fetch_allocation_results

def parse_labchip_file(plate_id, experiment_id, file):
    """
        Is responsible for orchestrating gathering of information
        about labchip wells and tagging labchip wells to the correct qpcr well

        Needs allocation results to trace labchip well to its parent qpcr well
         Needs  the set of 'wells' under mentioned experiment ,plate to use
         as key to pick information from labchip results

         Utilizes LabChipPeakProcessor to retrieve information from incoming
        file object.
        Orchestrates extraction of peak data from labchip results
        """

    labchip_reader = LabChipPeakProcessor()
    labchip_results = labchip_reader.parse_labchip_peak_data(file)
    allocation_results = fetch_allocation_results(experiment_id)
    wells = fetch_wells(allocation_results.source_map[plate_id])
    results = []
    for well_id in wells:
        if well_id in labchip_results:
            labchip_well = labchip_results[well_id]
            peaks = _extract_peaks(labchip_well, well_id,
                                   allocation_results.source_map[plate_id],
                                   plate_id)
            results = results + peaks
    return results

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

def _extract_peaks(labchip_well, well_id,source_map,plate_id):
    """
    orchestrates finding of source plate well for each labchip well ,
    normalizes peak data and aggregates peak results
    """
    peaks = []
    for peak_name, peak_data in labchip_well.items():

        source_well,source_plate = _get_source_plate_well(well_id,source_map)
        qpcr_well = fetch_qpcr_well(source_plate, source_well)
        peaks.append({
            'experiment':qpcr_well.experiment_id,
            'labchip_plate_id':plate_id,
            'size':_normalize_peak_data(peak_data,'size_[bp]'),
            'concentration':_normalize_peak_data(peak_data,'conc_('
                                                                 'ng/ul)'),
            'purity': _normalize_peak_data(peak_data,'%_purity'),
            'peak_name': peak_name,
            'molarity': _normalize_peak_data(peak_data,'molarity_('
                                                            'nmol/l)'),
            'labchip_well': peak_data['well_label'],
            'qpcr_well': qpcr_well.id
        })

    return peaks





def _get_source_plate_well(well_position,plate_allocation):
    """
    when called returns informations about source well and source plate
    governs conversion of well position from alphanumeric to numeric and
    vice versa
    """

    row, col = well_position_to_numeric(well_position)
    source_info = plate_allocation[col][row]

    source_well=well_position_to_alpha_numeric((source_info['source_row'],
                                              source_info['source_col']))

    source_plate = source_info['source_plate']

    return source_well,source_plate



def _normalize_peak_data(peak_data,key):
    """
    Replaces NaN with None
    """
    if math.isnan(peak_data[key]):
        return None
    return peak_data[key]


