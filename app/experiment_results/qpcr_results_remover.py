from app.models.labchip_results_model import LabChipResultsModel
from app.models.reagent_group_well_lookup_model import ReagentGroupWellLookupModel
from app.models.reagent_well_lookup_model import ReagentWellLookupModel
from django.db import transaction
from django.db.models.deletion import ProtectedError


def remove_qpcr_data(qpcr_query):
    """
    Performs removal of qpcr well related information from the data base
    assumes that any labchip well associated with the qpcr well to be deleted
    are already removed
    if not it will throw an error asking user to remove the lab chip records
    first
    On successful deletion returns count of wells deleted
    """
    well_ids = qpcr_query.values_list('id', flat=True)
    record_count = len(well_ids)
    try:
        with transaction.atomic():
            ReagentGroupWellLookupModel.objects.filter(
                well_id__in=well_ids).delete()
            ReagentWellLookupModel.objects.filter(
                well_id__in=well_ids).delete()
            qpcr_query.delete()
    except ProtectedError:
        labchip_plates = \
            LabChipResultsModel.objects.filter(
                qpcr_well__in=well_ids).values_list(
                'labchip_plate_id', flat=True).distinct()
        message = 'Unable to delete ,Pleas Delete Labchip plate {} ' \
                  'first'.format(','.join(labchip_plates))

        return {'msg': message}

    return {'msg': 'Deleted {} records in qpcr results'.format(record_count)}