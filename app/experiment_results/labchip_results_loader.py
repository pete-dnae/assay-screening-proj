from app.experiment_results.labchip_results_processor import \
    parse_labchip_file
from app.serializers import LabChipResultsSerializer

def load_labchip_results(experiment_id,plate_id,file):

    labchip_results = parse_labchip_file(plate_id,experiment_id,file)
    serializer =LabChipResultsSerializer(data=labchip_results, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer.data