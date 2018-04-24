
from clients.utils import get_object

from typing import List, Dict
DbReagent = List[str]
Reagent = Dict[str, str]


def reformat_db_reagent(db_reagent: DbReagent) -> Reagent:
    """
    Converts a datatbase reagent entry (a list of strings) to a dictionary with
    verbose keys.

    :param db_reagent: a list with three string values (as retrieved from an
    API call)
    :return:
    """
    r = {'reagent_name':  db_reagent[0],
         'concentration': db_reagent[1],
         'unit': db_reagent[2]}
    if r['reagent_name'].startswith('Transfer'):
        r['reagent_category'] = 'transfer'
    else:
        r['reagent_category'] = get_reagent_category(db_reagent[0])
    return r


def cached_reformat_db_reagent(db_reagent: DbReagent,
                               reagent_cache: Dict[str, Reagent]) -> Reagent:
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
    Reagent instances
    :return:
    """
    reagent_name = db_reagent[0]
    if reagent_name in reagent_cache:
        return reagent_cache[reagent_name]
    else:
        r = reformat_db_reagent(db_reagent)
        reagent_cache[r['reagent_name']] = r
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
        obj = obj[0]
        category = get_object(obj['category'])['name']
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
        r = get_object(obj['reagent'])
        c = get_object(r['category'])
        categories.add(c['name'])
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


def get_assays(reagents: List[Reagent]) -> List[Reagent]:
    """
    Extracts from a list of Reagent instances those that are assays
    :param reagents: a list of Reagent instances
    :return:
    """
    assays = [r for r in reagents if 'assay' in r['reagent_category']]
    return assays


def get_templates(reagents: List[Reagent]) -> List[Reagent]:
    """
    Extracts from a list of Reagent instances those that are templates
    :param reagents: a list of Reagent instances
    :return:
    """
    templates = [r for r in reagents if 'templates' in r['reagent_category']]
    return templates
