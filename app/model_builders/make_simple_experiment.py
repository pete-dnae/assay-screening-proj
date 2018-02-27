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


    def create(self):
        CreateExperiment()._create_concentrations()
        self.__create_reagents()
        self.experiment = self.__assemble_experiment()

        return self.experiment

    #-----------------------------------------------------------------------
    # Private below.
    #-----------------------------------------------------------------------


    def __create_reagents(self):
        finder = Finders()
        Reagent.make('DNA Free Water', '22884100', finder._conc_rat(1, 1, 'X'))
        for  primer_name in (('Eco63'),('Eco64'),('Eco60'),('Eco66')):
            Reagent.make(primer_name, '-', finder._conc_rat(1, 0.4, 'microM'))


    def __create_rules(self):
        cm = CommonModules()
        data = "V 1 \n" \
              "P1 \n" \
              "A DNA-free-Water            1-12    A-H 3.35 x \n" \
              "A Titanium-PCR-Buffer       1-12    A-H 0.63 x \n"
        return cm._rules_from_data(data)

    def __assemble_experiment(self):
        cm = CommonModules()
        return Experiment.make(
            'reference_experiment_1',
            'PH',
            ,
               cm._create_pa_cycling(),
               cm._create_id_cycling(),
        )


if __name__ == "__main__":
    SimpleExperiment().create()