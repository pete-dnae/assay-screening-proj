from pdb import set_trace as st

"""
Creates the minimum viable starter content for a virgin database.
With one experiment and only its dependents.
"""

from app.models.experiment_model import ExperimentModel
from app.models.rules_script_model import RulesScriptModel
from app.models.reagent_model import ReagentModel
from app.models.reagent_category_model import ReagentCategoryModel
from app.models.reagent_group_model import ReagentCategoryModel
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
        rules_script = RulesScriptModel.make(REFERENCE_SCRIPT)
        self.experiment = ExperimentModel.make(
                'Reference Experiment', rules_script)

        for units in REFERENCE_UNITS:
            UnitsModel.make(units)

        cats = {} # categories cache
        for reagent, cat_name in REFERENCE_REAGENTS_DATA:
            cat = cats[cat_name] if cat_name in cats else \
                    cats.setdefault(cat_name, 
                    ReagentCategoryModel.make(cat_name))
            ReagentModel.make(reagent, cat)

        return self.experiment

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------


if __name__ == "__main__":
    ReferenceExperiment().create()
