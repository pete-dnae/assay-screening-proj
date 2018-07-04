from app.experiment_results.labchip_results_processor import \
    parse_labchip_file
from app.serializers import LabChipResultsSerializer
from app.models import LabChipResultsModel
from rest_framework.exceptions import ValidationError
from django.db import transaction

def load_labchip_results(experiment_id,plate_id,file):
    assert_duplicate(plate_id,experiment_id)

    labchip_results = parse_labchip_file(plate_id,experiment_id,file)

    try:
        with transaction.atomic():
            serializer =LabChipResultsSerializer(data=labchip_results, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
    except:
        raise ValidationError('Labchip results write failed , Operation '
                              'reversed')
    response = get_labchip_upload_response(labchip_results)
    return response

def get_labchip_upload_response(labchip_results):
    experiment_id = set([record['experiment']for record in labchip_results])
    plate_id = set([record['labchip_plate_id']for record in labchip_results])
    wells = [record['labchip_well']for record in labchip_results]
    return {'wells': wells, 'experiment_id': experiment_id,
            'plate_id': plate_id}

def assert_duplicate(plate_id,experiment_id):
    query_set = LabChipResultsModel.objects.filter(labchip_plate_id =plate_id,
                                                   experiment_id =
                                                   experiment_id)
    if query_set.exists():
        raise ValidationError('Labchip results already exists')