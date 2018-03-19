"""
Creates the minimum viable starter content for a virgin database.
With one experiment and only its dependents.
"""

from app.models.experiment_model import ExperimentModel
from app.models.rules_script_model import RulesScriptModel
from app.model_builders.reference_rules_script import REFERENCE_SCRIPT


class ReferenceExperiment():
    """
    Creates all the database entities required to assemble an example,
    refrence models.Experiment, and returns the correpsonding instance.
    """

    def __init__(self):
        self.experiment = None

    def create(self):
        rules_script = RulesScriptModel.make( REFERENCE_SCRIPT)
        self.experiment = ExperimentModel.make(
                'Reference Experiment', rules_script)
        return self.experiment

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------


if __name__ == "__main__":
    ReferenceExperiment().create()
