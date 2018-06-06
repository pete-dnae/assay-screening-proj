from pdb import set_trace as st

from app.models.experiment_model import ExperimentModel
from app.models.rules_script_model import RulesScriptModel
from app.models.reagent_model import ReagentModel
from app.models.reagent_category_model import ReagentCategoryModel
from app.models.reagent_group_model import ReagentGroupModel
from app.models.reagent_group_model import ReagentGroupDetailsModel
from app.models.units_model import UnitsModel
from app.model_builders.reference_data import REFERENCE_SCRIPT
from app.model_builders.reference_data import REFERENCE_REAGENTS_DATA
from app.model_builders.reference_data import REFERENCE_GROUP
from app.model_builders.reference_data import REFERENCE_UNITS


class ReferenceExperiment():
    """
    Creates all the database entities required to assemble an example,
    refrence models.Experiment, and returns the correpsonding instance.
    Aborts and does nothing if the experiment already exists in the databse.
    """

    def __init__(self):
        self.experiment = None

    def create(self):
        if self._already_exists_in_db():
            return

        # A rules script
        rules_script = RulesScriptModel.make(REFERENCE_SCRIPT)

        # An experiment
        self.experiment = ExperimentModel.make(
                self._REFERENCE_EXPERIMENT, 'vanilla' ,rules_script)

        # Approved concentration units.
        for units in REFERENCE_UNITS:
            UnitsModel.make(units)

        # Reagent categories, and reagents
        categories = {}
        for reagent, cat_name,opaque_payload in REFERENCE_REAGENTS_DATA:
            # Have to avoid creating duplicate category objects.
            cat = categories.get(cat_name, None)
            if cat is None:
                cat = ReagentCategoryModel.make(cat_name)
                categories[cat_name] = cat
            ReagentModel.make(reagent, cat,opaque_payload)

        # Make a primer group with two of the primers in.
        group_name = REFERENCE_GROUP['name']
        ReagentGroupModel.make(group_name)
        for member_name, conc, units in REFERENCE_GROUP['members']:
            reagent = ReagentModel.objects.get(name=member_name)
            units = UnitsModel.objects.get(abbrev=units)
            reagent_group = ReagentGroupModel(group_name=group_name)
            ReagentGroupDetailsModel.make(reagent_group, reagent, conc, units)


        return self.experiment

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    _REFERENCE_EXPERIMENT = 'Reference Experiment'

    def _already_exists_in_db(self):
        try:
            ExperimentModel.objects.get(
                experiment_name=self._REFERENCE_EXPERIMENT)
        except ExperimentModel.DoesNotExist:
            return False
        return True


if __name__ == "__main__":
    ReferenceExperiment().create()
