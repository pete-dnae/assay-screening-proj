from app.serializers import *
from app.experiment_results.qpcr_results_processor import parse_qpcr_file

def load_qpcr_results(experiment_id,plate_name,file):
    results, reagents_used, reagent_group_used = \
        parse_qpcr_file(plate_name,experiment_id,file)

    for record in results:
        instance = validate_create_qpcr_result_record(record)
        if instance.qpcr_well in reagents_used:
            validate_create_reagent_lookup(instance,reagents_used)
        if instance.qpcr_well in reagent_group_used:
            validate_create_reagent_group_lookup(instance,reagent_group_used)

    return results

def validate_create_reagent_lookup(instance,reagents_used):

    for reagent in reagents_used[instance.qpcr_well]:
        reagent['well'] = instance.id
        reagent_serializer = ReagentWellLookupSerializer(
            data=reagent)
        reagent_serializer.is_valid(raise_exception=True)
        reagent_serializer.save()


def validate_create_reagent_group_lookup(instance,reagent_group_used):

    for reagent_group in reagent_group_used[instance.qpcr_well]:
        reagent_group['well'] = instance.id
        reagent_group_serializer = ReagentGroupWellLookupSerializer(
            data=reagent_group)
        reagent_group_serializer.is_valid(raise_exception=True)
        reagent_group_serializer.save()

def validate_create_qpcr_result_record(record):

    qpcr_serializer = QpcrResultsSerializer(data=record)
    qpcr_serializer.is_valid(raise_exception=True)
    instance = qpcr_serializer.save()

    return instance