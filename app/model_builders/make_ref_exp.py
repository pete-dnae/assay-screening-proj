from pdb import set_trace as st

"""
Creates the minimum viable starter content for a virgin database.
With one experiment and only its dependents.
"""

from app.models.experiment_model import ExperimentModel
from app.models.rules_script_model import RulesScriptModel
from app.models.reagent_model import ReagentModel
from app.models.reagent_category_model import ReagentCategoryModel
from app.models.reagent_group_model import ReagentGroupModel
from app.models.units_model import UnitsModel
from app.model_builders.reference_data import REFERENCE_SCRIPT
from app.model_builders.reference_data import REFERENCE_REAGENTS_DATA
from app.model_builders.reference_data import REFERENCE_GROUP
from app.model_builders.reference_data import REFERENCE_UNITS


class ReferenceExperiment():
    """
    Creates all the database entities required to assemble an example,
    refrence models.Experiment, and returns the correpsonding instance.
    """

    def __init__(self):
        self.experiment = None

    def create(self):
        # A rules script
        rules_script = RulesScriptModel.make(REFERENCE_SCRIPT)

        # An experiment
        self.experiment = ExperimentModel.make(
                'Reference Experiment', rules_script)

        # Approved concentration units.
        for units in REFERENCE_UNITS:
            UnitsModel.make(units)

        # Reagent categories, and reagents
        categories = {}
        for reagent, cat_name in REFERENCE_REAGENTS_DATA:
            # Have to avoid creating duplicate category objects.
            cat = categories.get(cat_name, None)
            if cat is None:
                cat = ReagentCategoryModel.make(cat_name)
                categories[cat_name] = cat
            ReagentModel.make(reagent, cat)

        # Make a primer group with two of the primers in.
        group_name = REFERENCE_GROUP['name']
        for member_name, conc, units in REFERENCE_GROUP['members']:
            reagent = ReagentModel.objects.get(name=member_name)
            units = UnitsModel.objects.get(abbrev=units)
            ReagentGroupModel.make(group_name, reagent, conc, units)


        return self.experiment

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------


if __name__ == "__main__":
    ReferenceExperiment().create()
