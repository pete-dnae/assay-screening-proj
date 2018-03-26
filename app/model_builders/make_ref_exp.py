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

        # Make a strains groups that includes both the strain
        # reagents we created above.
        reagents = ReagentModel.objects.filter(category__name='Strain')
        category = ReagentCategoryModel.objects.get(name='Strain')
        ReagentGroupModel.make('Strain', category, reagents)




        return self.experiment

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------


if __name__ == "__main__":
    ReferenceExperiment().create()
