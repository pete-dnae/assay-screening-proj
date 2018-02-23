"""
Creates a simple experiment with very minimal starting content
"""

from app.models.reagent_models import *
from app.models.primer_models import *
from app.models.strain_models import *
from app.models.experiment_model import *
from app.models.rule_models import *
from app.model_builders.finders import Finders
from app.model_builders.common_modules import CreateExperiment

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
        finder = Finders()
        experiment = CreateExperiment()
        data = (((finder._reagent(Reagent.make_hash('Eco64', Concentration.value_from_quotient(1, 0.4))),
                  ('A', 'A', 1, 2)),
                 (finder._reagent(Reagent.make_hash('Eco63', Concentration.value_from_quotient(1, 0.4))),
                  ('A', 'A', 1, 2)),
                 (finder._reagent(Reagent.make_hash('DNA Free Water', Concentration.value_from_quotient(1, 1))),
                  ('A', 'B', 1, 2)),
                 ))
        return experiment._rules_from_data('Reagent', data)

    def __assemble_experiment(self):
        experiment = CreateExperiment()
        return Experiment.make(
            'reference_experiment_1',
            'PH',
            [Plate.make(
                'reference_experiment_1' + '_1',
                AllocationInstructions.make(
                    RuleList.make(self.__create_rules()),
                    '4, 8, 12'
                )
            )],
            experiment._create_pa_cycling(),
            experiment._create_id_cycling(),
        )


if __name__ == "__main__":
    SimpleExperiment().create()