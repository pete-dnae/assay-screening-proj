from app.models.reagent_model import ReagentModel
from app.models.units_model import UnitsModel
from app.models.reagent_group_model import ReagentGroupModel
from app.models.experiment_model import ExperimentModel
from app.rules_engine.rule_script_processor import RulesScriptProcessor
from app.models.reagent_group_model import ReagentGroupDetailsModel
from django.shortcuts import get_object_or_404
from json.decoder import JSONDecodeError
from rest_framework.exceptions import ValidationError
import json
from .labchip_results_processor import UnexpectedWellNameError
import re
from collections import defaultdict

def fetch_labchip_data(query_set):
    qpcr_labchip_lookup = get_qpcr_well_lookup(query_set)
    labchip_results = get_labchip_results_from_queryset(query_set)
    labchip_wells = get_labchip_wells(query_set)
    labchip_plate_id = get_labchip_palate_id(query_set)

    return qpcr_labchip_lookup,labchip_results,labchip_results,labchip_plate_id


def get_qpcr_well_lookup(query_set,qpcr_well_map):
    """
    Returns a dictionary keyes by qpcr wells with values corresponding to
    labchip wells
    """
    labchip_lookup_dict = {record['qpcr_well_id']: record['labchip_well']
                           for record in query_set.values('qpcr_well_id',
                                                          'labchip_well')}
    qpcr_lookup_dict = {}

    for qpcr_well_id, qpcr_well in qpcr_well_map.items():
        qpcr_lookup_dict[qpcr_well] = labchip_lookup_dict[qpcr_well_id] if \
            qpcr_well_id in labchip_lookup_dict else None

    return qpcr_lookup_dict



def get_labchip_results_from_queryset(query_set):
    """
    returns a restructured form of labchip resutls extractd from queryset
    """
    results = defaultdict(dict)

    for labchip in query_set.values():
        peak_dict = results[labchip['labchip_well']].setdefault('peak', {})
        key = labchip['peak_name']
        peak_dict[key] = {'%_purity': labchip['purity'],
                          'conc_(ng/ul)': labchip['concentration'],
                          'molarity_(nmol/l)': labchip['molarity'],
                          'size_[bp]': labchip['size']
                          }

    return results

def get_labchip_wells(query_set):

    return [result['labchip_well'] for result in query_set.values(
        'labchip_well')]

def get_labchip_palate_id(query_set):

    labchip_record = query_set.first()
    if labchip_record:
        return labchip_record.labchip_plate_id

    return None


def fetch_qpcr_data(query_set):

    qpcr_well_ids = get_qpcr_well_ids(query_set)
    qpcr_results = get_qpcr_results_by_well(query_set)

    return qpcr_results,qpcr_well_ids

def get_qpcr_well_ids(query_set):
    """
    Prepares a dictionary with well db id as key and well name as value
    """
    return {record['id']: record['qpcr_well'] for record in
            query_set.values('id', 'qpcr_well')}

def get_qpcr_results_by_well(query_set):
    """
    Prepares a dictionary with well name as key and well results as value
    """

    return {result['qpcr_well']: result for result in query_set.values()}


def fetch_allocation_results(experiment_id):
    """
      Fetches experiment ,prepares allowed reagents and units.
      Co-ordinates interpretation of ruleScript to produce allocation
      results.
      Returns None if errors are present
    """
    experiment = fetch_experiment(experiment_id)
    reagent_names = [r.name for r in ReagentModel.objects.all()]

    group_names = set([g.group_name for g in \
                       ReagentGroupModel.objects.all()])

    allowed_names = reagent_names + list(group_names)
    units = [u.abbrev for u in UnitsModel.objects.all()]

    interpreter = RulesScriptProcessor(
        experiment.rules_script.text, allowed_names, units)
    parse_error, alloc_table, thermal_cycling_results, line_num_mapping = \
        interpreter.parse_and_interpret()

    return None if not alloc_table else alloc_table

def fetch_experiment(experiment_id):
    """"
      Fetches experiment object from db , returns http:404 if not fould
    """
    return get_object_or_404(ExperimentModel, pk=experiment_id)

def fetch_reagent_data(query_set):


    reagent_category = fetch_reagent_categories(query_set)
    assay_amplicon_lengths = fetch_assay_amplicon_lengths(
        query_set)
    return reagent_category,assay_amplicon_lengths

def fetch_reagent_categories():
    """
    returns reagents and reagent groups from db , along with their
    category information
    """
    reagent_category = {r.name: r.category.name for r in
                        ReagentModel.objects.all()}

    for r in ReagentGroupModel.objects.all():
        group_element = ReagentGroupDetailsModel.objects.filter(
            reagent_group=r.group_name).first()
        reagent_category[r.group_name] = group_element.reagent.category.name

    return reagent_category

def fetch_assay_amplicon_lengths():
    query_set=ReagentModel.objects.filter(category_id='assay')
    amplicon_len_dict = {}
    for element in query_set:
        json_string = element.opaque_json_payload
        try:
            if json_string is None:
                raise ValueError('opaque payload for assay not found')
            meta_data = json.loads(json_string)
            if 'amplicon_length' in meta_data:
                amplicon_len_dict[element.name] = float(meta_data[
                                                            'amplicon_length'])
        except JSONDecodeError:
            raise ValidationError
    return amplicon_len_dict

def get_dilutions(plate_allocation, labchip_wells):
    dilution_dict = {}
    for well_id in labchip_wells:
        row, col = well_position_to_numeric(well_id)
        well_allocation = plate_allocation[col][row]
        dilutions = [conc for (reagent, conc, unit) in well_allocation if
                     unit == 'dilution']
        if len(dilutions) > 0:
            dilution_dict[well_id] = dilutions[0]
    return dilution_dict

def well_position_to_numeric( well_position):
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

