from typing import List

from clients.reagents import Reagent
from clients.vessels import row_col_to_well, Plates


def decode_transfer_to_plate_well(transfer_str: str):
    """
    Decodes a transfer string to plate and well value
    :param transfer_str: a transfer string
    :return:
    """
    transfer_str = transfer_str.split()[1]
    plate, cidx, ridx = transfer_str.split(':')
    cidx = int(cidx.replace('Col-', ''))
    ridx = int(ridx.replace('Row-', ''))
    well = row_col_to_well(ridx, cidx)
    return plate, well


def get_transferred_reagents(transfer_str: str, plates: Plates):
    """
    Extracts a list of Reagent instance from a Plates dictionary as specified in
    the transfer string
    :param transfer_str: a transfer string
    :param plates: a Plates dictionary
    :return:
    """
    plate, well = decode_transfer_to_plate_well(transfer_str)
    transferred_reagents = plates[plate][well]
    return transferred_reagents


def filter_transferred_reagents(transfer_str: str,
                                plates: Plates,
                                reagent_category: str):
    """
    Filter transferred reagents by category.
    :param transfer_str: a transfer string
    :param plates: a Plates dictionary
    :param reagent_category: reagent category string on which to filter
    :return:
    """
    transferred_reagents = get_transferred_reagents(transfer_str, plates)
    filtered_reagents = [r for r in transferred_reagents
                         if reagent_category in r['reagent_category']]
    return filtered_reagents


def get_transferred_assays(reagents: List[Reagent], plates: Plates):
    """
    Convenience function to get all transferred assays
    :param reagents: a list of Reagent instances
    :param plates: a Plates dictionary
    :return:
    """
    assays = []
    transfers = [r['reagent_name'] for r in reagents
                 if 'transfer' in r['reagent_category']]
    for trans in transfers:
        ass = filter_transferred_reagents(trans, plates, 'assay')
        assays = assays + ass
    return assays


def get_transferred_templates(reagents: List[Reagent], plates: Plates):
    """
    Convenience function to get all transferred templates
    :param reagents: a list of Reagent instances
    :param plates: a Plates dictionary
    :return:
    """
    templates = []
    transfers = [r['reagent_name'] for r in reagents
                 if 'transfer' in r['reagent_category']]
    for trans in transfers:
        temps = filter_transferred_reagents(trans, plates, 'templates')
        templates = templates + temps
    return templates
