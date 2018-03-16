"""
Creates the minimum viable starter content for a virgin database.
With one experiment and only its dependents.
"""

from app.models.experiment_model import Experiment
from app.models.rules_script_model import RulesScriptModel


class ReferenceExperiment():
    """
    Creates all the database entities required to assemble an example,
    refrence models.Experiment, and returns the correpsonding instance.
    """

    def __init__(self):
        self.experiment = None

    def create(self):
        rules_script = RulesScriptModel.make(
                ReferenceExperiment.REFERENCE_RULES_SCRIPT)
        self.experiment = Experiment.make(
                'Reference Experiment', rules_script)
        return self.experiment

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------


if __name__ == "__main__":
    ReferenceExperiment().create()
