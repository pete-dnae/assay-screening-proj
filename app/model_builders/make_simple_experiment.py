"""
Creates a simple experiment with very minimal starting content
"""

from app.models.reagent_models import *
from app.models.primer_models import *
from app.models.strain_models import *
from app.models.experiment_model import *
from app.models.rule_models import *
from app.model_builders.finders import Finders
from app.model_builders.common_modules import CommonModules

class SimpleExperiment():
    """
    creates all DB entities necessary to assembe a simple experiment
    """

    def __init__(self):
        self.experiment = None
        self.script = "V 1 \n" \
                          "P1 \n" \
                          "A DNA-free-Water            1-12    A-H 3.35 x \n" \
                          "A Titanium-PCR-Buffer       1-12    A-H 0.63 x \n"

    def create(self):
        self.experiment = self.__assemble_experiment()
        return self.experiment

    #-----------------------------------------------------------------------
    # Private below.
    #-----------------------------------------------------------------------




    def __assemble_experiment(self):
        cm = CommonModules()
        cm.validate_rules(self.script)

        return Experiment.make(
            'reference_experiment_1',
            'PH',
            RuleScript.make(
                self.script
            ),
               cm.create_pa_cycling(),
               cm.create_id_cycling(),
        )


if __name__ == "__main__":
    SimpleExperiment().create()