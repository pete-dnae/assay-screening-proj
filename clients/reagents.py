
from clients.utils import get_object

from typing import List, Dict, Tuple
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


def disambiguate_templates(templates: List[ObjReagent]):
    """
    Separate templates into human and other categories.
    :param templates: a list of reagent objects that have been pre-filtered to
    only those that are of category type: `template`
    :return:
    """
    human = []
    other = []
    for t in templates:
        if 'hgdna' in t['reagent_name'].lower():
            human.append(t)
        else:
            other.append(t)
    return human, other
