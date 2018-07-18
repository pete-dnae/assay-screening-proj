from django.db import transaction

def remove_labchip_data(labchip_query):
    """
    Deletes the records in the given query set ,
    if successful it will return the count of distinct labchip wells deleted
    if things go wrong it will revert the deletion and throw an error
    """
    with transaction.atomic():

        well_count = len(labchip_query.values_list('labchip_well').distinct())
        labchip_query.delete()
        message =  {'msg': 'Deleted {} wells in labchip results'.format(
            well_count)} 
        return message