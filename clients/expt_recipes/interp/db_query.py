
from clients.utils import get_object
import json

from typing import List, Dict, Tuple, Any
from hardware.plates import row_col_to_well, ExptPlates

DbReagent = List[str]
ObjReagent = Dict[str, str]


def db_reagent_2_obj_reagent(db_reagent: DbReagent) -> ObjReagent:
    """
    Converts a datatbase reagent entry (a list of strings) to a dictionary with
    verbose keys.

    :param db_reagent: a list with three string values (as retrieved from an
    API call)
    :return:
    """
    r = {'reagent_name': db_reagent[0],
         'concentration': db_reagent[1],
         'unit': db_reagent[2]}
    if r['reagent_name'].startswith('Transfer'):
        r['reagent_category'] = 'transfer'
    else:
        r['reagent_category'] = get_reagent_category(db_reagent[0])
    return r


def cached_db_reagent_2_obj_reagent(
        db_reagent: DbReagent,
        reagent_cache: Dict[Tuple[str], ObjReagent]) -> ObjReagent:
    """
    A convenience function that prevents multiple API calls for reagents that
    have already been returned.

    example usage:
        reagent_cache = {}
        db_reagents = [...]  # a list of DbReagent instances
        reagents = []
        for reagent in db_reagents:
            r = cached_reformat(db_reagent(reagent, reagent_cache)
            reagents.append(r)

    :param db_reagent: an instance of a DbReagent
    :param reagent_cache: a dictionary that caches previously returned
    ObjReagent instances
    :return:
    """
    reagent_key = tuple(db_reagent)
    if reagent_key in reagent_cache:
        return reagent_cache[reagent_key]
    else:
        r = db_reagent_2_obj_reagent(db_reagent)
        reagent_cache[reagent_key] = r
        return r


def get_single_reagent_category(reagent_name: str) -> str:
    """
    Get the category for a given reagent.
    :param reagent_name: name of reagent
    :return:
    """
    obj = get_object(
        'https://assay-screening.herokuapp.com/api/reagents/?name={}'
        .format(reagent_name))
    if len(obj) == 1:
        category = obj[0]['category']
        return category
    else:
        raise ValueError('Could not determine reagent category for: {}'
                         .format(reagent_name))


def get_single_reagent_opaque_payload(reagent_name: str) -> Dict[str, Any]:
    """
    Get the category for a given reagent.
    :param reagent_name: name of reagent
    :return:
    """
    obj = get_object(
        'https://assay-screening.herokuapp.com/api/reagents/?name={}'
        .format(reagent_name))
    if len(obj) == 1:
        opaque_payload = obj[0]['opaque_json_payload']
        opaque_payload = json.loads(opaque_payload)
        return opaque_payload
    else:
        raise ValueError('Could not determine reagent payload for: {}'
                         .format(reagent_name))


def get_group_reagent_category(reagent_name: str) -> str:
    """
    Get the group category for a given reagent.
    :param reagent_name: name of reagent
    :return:
    """
    objs = get_object(
        'https://assay-screening.herokuapp.com/api/reagent-groups/?name={}'
        .format(reagent_name))
    categories = set()
    for obj in objs:
        categories.add(get_single_reagent_category(obj['reagent']))
    if len(categories) == 1:
        return list(categories)[0]
    else:
        raise ValueError('Group reagent {} consists of multiple different '
                         'reagent categories: {}'
                         .format(reagent_name, categories))


def get_reagent_category(reagent_name: str) -> str:
    """
    Get a reagents category.

    At first, will assume that the reagent is singular and hence get it's
    category. If that fails will then assume the reagent is a group reagent
    and then get that group's category.

    :param reagent_name: name of reagent
    :return:
    """
    try:
        category = get_single_reagent_category(reagent_name)
    except ValueError:
        category = 'group {}'.format(
            get_group_reagent_category(reagent_name))
    return category


def get_assays(reagents: List[ObjReagent]) -> List[ObjReagent]:
    """
    Extracts from a list of ObjReagent instances those that are assays
    :param reagents: a list of ObjReagent instances
    :return:
    """
    assays = [r for r in reagents if 'assay' in r['reagent_category']]
    return assays


def get_templates(reagents: List[ObjReagent]) -> List[ObjReagent]:
    """
    Extracts from a list of ObjReagent instances those that are templates
    :param reagents: a list of ObjReagent instances
    :return:
    """
    templates = [r for r in reagents if 'template' in r['reagent_category']]
    return templates


def get_humans(reagents: List[ObjReagent]) -> List[ObjReagent]:
    """
    Extracts from a list of ObjReagent instances those that are templates
    :param reagents: a list of ObjReagent instances
    :return:
    """
    humans = [r for r in reagents if 'human' in r['reagent_category']]
    return humans


def get_assay_amplicon_length(assay_name: str):
    """
    Gets the amplicon length value for a given assay.
    :param assay_name: asssay name
    :return:
    """
    payload = get_single_reagent_opaque_payload(assay_name)
    return payload['amplicon_length']


def decode_transfer_to_plate_well(transfer_str: str) -> Tuple[str, str]:
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


def get_transferred_reagents(transfer_str: str,
                             plates: ExptPlates) -> List[ObjReagent]:
    """
    Extracts a list of ObjReagent instance from a Plates dictionary as
    specified in the transfer string
    :param transfer_str: a transfer string
    :param plates: a Plates dictionary
    :return:
    """
    plate, well = decode_transfer_to_plate_well(transfer_str)
    transferred_reagents = plates[plate][well]
    return transferred_reagents


def filter_transferred_reagents(transfer_str: str,
                                plates: ExptPlates,
                                reagent_category: str) -> List[ObjReagent]:
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


def get_transferred_assays(reagents: List[ObjReagent],
                           plates: ExptPlates) -> List[ObjReagent]:
    """
    Convenience function to get all transferred assays
    :param reagents: a list of ObjReagent instances
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


def get_transferred_templates(reagents: List[ObjReagent],
                              plates: ExptPlates) -> List[ObjReagent]:
    """
    Convenience function to get all transferred templates
    :param reagents: a list of ObjReagent instances
    :param plates: a Plates dictionary
    :return:
    """
    templates = []
    transfers = [r['reagent_name'] for r in reagents
                 if 'transfer' in r['reagent_category']]
    for trans in transfers:
        temps = filter_transferred_reagents(trans, plates, 'template')
        templates = templates + temps
    return templates


def get_transferred_humans(reagents: List[ObjReagent],
                           plates: ExptPlates) -> List[ObjReagent]:
    """
    Convenience function to get all transferred templates
    :param reagents: a list of ObjReagent instances
    :param plates: a Plates dictionary
    :return:
    """
    humans = []
    transfers = [r['reagent_name'] for r in reagents
                 if 'transfer' in r['reagent_category']]
    for trans in transfers:
        hums = filter_transferred_reagents(trans, plates, 'human')
        humans = humans + hums
    return humans


def get_parent_wells(reagents) -> List[Tuple[str, str]]:
    parents = []
    for r in reagents:
        if r['reagent_name'].startswith('Transfer'):
            plate, well = decode_transfer_to_plate_well(r['reagent_name'])
            parents.append((plate, well))
    return parents


def get_dilutions(reagents) -> List[float]:
    dilutions = []
    for r in reagents:
        if r['reagent_name'].startswith('Transfer'):
            dilutions.append(r['concentration'])
    return dilutions
