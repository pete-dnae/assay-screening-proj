
import os
import json
from app.models.reagent_group_model import ReagentGroupDetailsModel

PATH = os.path.dirname(os.path.abspath(__file__))


def get_mastermixes():
    with open(os.path.join(PATH, 'mastermix.json'), 'r') as fp:
        layouts = json.load(fp)
    return layouts


def get_mastermix(mastermix):
    query_set = ReagentGroupDetailsModel.objects.filter(reagent_group=mastermix)
    mastermix_elements = [{'name':element.reagent.name,
                           'quantity':element.concentration,
                           'unit':element.units.abbrev} for element in
                          query_set]
    return mastermix_elements
