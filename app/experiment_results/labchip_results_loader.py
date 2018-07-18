from app.experiment_results.labchip_results_processor import \
    parse_labchip_file
from app.serializers import LabChipResultsSerializer
from app.models import LabChipResultsModel
from rest_framework.exceptions import ValidationError
from django.db import transaction

def load_labchip_results(experiment_id,plate_id,file):
    assert_duplicate_plate(plate_id,experiment_id)

    labchip_results = parse_labchip_file(plate_id,experiment_id,file)


    with transaction.atomic():
        assert_duplicate_well(labchip_results,plate_id)
        serializer =LabChipResultsSerializer(data=labchip_results, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    response = get_labchip_upload_response(labchip_results)
    return response

def get_labchip_upload_response(labchip_results):
    experiment_id = set([record['experiment']for record in labchip_results])
    plate_id = set([record['labchip_plate_id']for record in labchip_results])
    wells = sorted(set([record['labchip_well']for record in labchip_results]))

    return {'wells': wells, 'experiment_id': experiment_id,
            'plate_id': plate_id}

def assert_duplicate_plate(plate_id,experiment_id):
    query_set = LabChipResultsModel.objects.filter(labchip_plate_id =plate_id,
                                                   experiment_id =
                                                   experiment_id)
    if query_set.exists():
        raise ValidationError('Labchip results already exists')

def assert_duplicate_well(labchip_results,plate_id):
    labchip_well_names = [record['labchip_well'] for record in labchip_results]
    qpcr_well_ids = [record['qpcr_well'] for record in labchip_results]
    duplicate_lc_wells = \
        LabChipResultsModel.objects.filter(labchip_plate_id = plate_id,
                                           labchip_well__in=labchip_well_names)
    duplicate_qpcr_wells = LabChipResultsModel.objects.filter(
        qpcr_well__in=qpcr_well_ids)

    if duplicate_lc_wells.exists():
        experiment = duplicate_lc_wells.values_list('experiment',
                                                    flat=True).distinct()
        labchip_wells = duplicate_lc_wells.values_list('labchip_well',
                                                       flat=True).distinct()
        message =\
            'Labchip wells {} already exist in experiment {}'\
                .format(','.join(labchip_wells),','.join(experiment))
        raise ValidationError(message)

    if duplicate_qpcr_wells.exists():
        experiment = duplicate_qpcr_wells.values_list('experiment',
                                                    flat=True).distinct()
        labchip_plate = duplicate_qpcr_wells.values_list('labchip_plate_id',
                                                       flat=True).distinct()
        message = \
            'Qpcr wells already mapped to LC Plate {} from ' \
            'experiment {}' \
                .format(','.join(labchip_plate), ','.join(experiment))
        raise ValidationError(message)