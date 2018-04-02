from pdb import set_trace as st

from app.models.reagent_model import ReagentModel
from app.models.reagent_group_model import ReagentGroupModel
from app.models.units_model import UnitsModel


class BatchGroupsEntry():
    """
    Utility class to input multiple reagent groups into the database.
    """

    def __init__(self):
        pass

    def load_db(self, groups):
        """
        Define the groups you want to create using a data structure
        like this, keyed on group name:

            groups = {
                'Pool-1': (
                    ('reagent_1', 0.4, 'M/uL'),
                    ('reagent_2', 0.1, 'M/uL'),
                ),
                'Pool-2': (
                    ('reagent_1', 0.8, 'M/uL'),
                    ('reagent_2', 0.2, 'M/uL'),
                )
            }

        The reagents must pre-exist.
        The units strings must be from those pre-registered in the system.
        """
        for group_name, member_rows in groups.items():
            for row in member_rows:
                self._process_row(row, group_name)

    def _process_row(self, row, group_name):
        reagent_name, conc, units =  row
        try:
            reagent_obj = ReagentModel.objects.get(name=reagent_name)
        except ReagentModel.DoesNotExist:
            raise RuntimeError('Reagent: <%s> does not exist' % reagent_name)
        try:
            units_obj = UnitsModel.objects.get(abbrev=units)
        except UnitsModel.DoesNotExist:
            raise RuntimeError('Units: <%s> does not exist' % units)
        ReagentGroupModel.make(group_name, reagent_obj, conc, units_obj)
