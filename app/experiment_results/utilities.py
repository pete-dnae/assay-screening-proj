import re

class UnexpectedWellNameError(Exception):
    pass

def well_position_to_numeric(well_position):
    """
    Converts well position from alphanumeric to numeric
    """

    match = re.match(r"([A-Z])([0-9]+)", well_position)

    if not match:
        raise UnexpectedWellNameError()

    try:
        row, col = match.groups()
        numrow = ord(row) - 64
        numcol = int(col)
        return numrow, numcol
    except:
        raise UnexpectedWellNameError()

def get_qpcr_labchip_well_map(qpcr_query,labchip_query):

    qpcr_labchip_well_map = {record.qpcr_well: None for record in
                             qpcr_query}
    if labchip_query.exists():
        qpcr_labchip_dict = {record.qpcr_well.qpcr_well: record.labchip_well for
                             record in labchip_query}
        qpcr_labchip_well_map.update(qpcr_labchip_dict)

    return qpcr_labchip_well_map

def well_position_to_alpha_numeric(well_position):
    """
    Converts well position from numeric to alphanumeric
    """
    row, col = well_position
    strcol = str(col).zfill(2)
    strrow = chr(row + 64)
    return strrow + strcol

def fetch_wells(plate_info):
    """
    Extracts keys from allocation_results and convert them into
    corresponding alphanumeric well_name representations
    """
    wells = []

    for col,rows in plate_info.items():
        wells_in_row =[well_position_to_alpha_numeric((row,col)) for row in
                       rows.keys()]
        wells = wells+wells_in_row
    return set(wells)