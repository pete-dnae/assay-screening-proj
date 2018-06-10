from app.models import *
from app.rules_engine.rule_script_processor import RulesScriptProcessor
from app.models.reagent_group_model import ReagentGroupDetailsModel
from django.shortcuts import get_object_or_404
from json.decoder import JSONDecodeError
from rest_framework.exceptions import ValidationError
import json
from .utilities import UnexpectedWellNameError
import re
import ast
from collections import defaultdict
from clients.expt_recipes.lost import build_labchip_datas_from_inst_data
from django.db import connection
from app.experiment_results.result_aggregation_query import GroupByIDAssay

def get_labchip_query(qpcr_query):
    """
    Returns query which represent labchip wells associated to the given qpcr
    query
    """
    qpcr_well_db_ids = qpcr_query.values_list('id', flat=True)
    labchip_query_set = \
        LabChipResultsModel.objects.filter(qpcr_well__in=qpcr_well_db_ids)
    return labchip_query_set

def get_qpcr_query_from_meta(meta):
    """
    Returns a qpcr query from meta information passed
    """
    wells = meta['wells'].split(",")
    qpcr_query = \
        QpcrResultsModel.objects.filter(experiment_id=meta['experiment_id'],
        qpcr_plate_id=meta['qpcr_plate_id'],qpcr_well__in=wells)

    return qpcr_query

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
    """
    Returns amplicon length meta field for all the assay type reagents
    present in database
    """
    query_set = ReagentModel.objects.filter(category_id = 'assay')
    amplicon_len_dict = {}
    for element in query_set:
        json_string = element.opaque_json_payload
        try:
            if json_string is not None:
                meta_data = json.loads(json_string)
                if 'amplicon_length' in meta_data:
                    amplicon_len_dict[element.name] = float(meta_data[
                                                                'amplicon_length'])
        except JSONDecodeError:
            raise ValidationError
    return amplicon_len_dict

def get_dilutions(labchip_query):
    """
    Preapares data required to calculate dilutions from the passed in labchip
    query
    """
    if labchip_query.exists():
        labchip_record = labchip_query.first()
        allocation_results = fetch_allocation_results(labchip_record.experiment_id)
        labchip_wells = labchip_query.values_list('labchip_well',flat=True)
        dilutions = make_dilution(
            allocation_results.plate_info[labchip_record.labchip_plate_id],
            labchip_wells)
        return dilutions
    else:
        return None

def make_dilution(plate_allocation,labchip_wells):
    """
    Returns the dilution amounts from plate allocation for the given
    labchip wells
    """
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

def fetch_qpcr_well(qpcr_plate, qpcr_well):
    """"
    Fetches qpcr well object from db , returns http:404 if not fould
    """
    return get_object_or_404(QpcrResultsModel,
                             qpcr_plate_id=qpcr_plate,
                             qpcr_well=qpcr_well)


def get_labchip_results_by_well(well_constituents, labchip_query):
    """
    Preapares labchip wells related data required to build labchip data
    container and builds them
    """

    reagent_amplicon_lenghts = fetch_assay_amplicon_lengths()
    qpcr_labchip_well_map = \
        {record.qpcr_well.qpcr_well: record.labchip_well for record in
         labchip_query}
    labchip_results = get_labchip_results_from_queryset(labchip_query)
    dilutions = get_dilutions(labchip_query)
    labchip_data = \
        build_labchip_datas_from_inst_data(well_constituents,
                                           labchip_results,
                                           qpcr_labchip_well_map,
                                           reagent_amplicon_lenghts,
                                           dilutions)
    return labchip_data


def get_labchip_plate_id(labchip_query):
    """
    returns labchip plate id from labchip query passed
    """

    if labchip_query.exists():
        labchip_record = labchip_query.first()
        return labchip_record.labchip_plate_id
    else:
        return None

def get_wells_grouped_by_id_assay():
    """
    Runs a raw sqpl query to get wells and their meta properties grouped by
    ID Assay
    Doesnt care about meta properties check query to find fields retrieved
    """
    with connection.cursor() as cursor:
        cursor.execute(GroupByIDAssay)
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]