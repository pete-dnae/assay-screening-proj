"""
Creates a simple experiment with very minimal starting content
"""

from app.models.reagent_models import *
from app.models.primer_models import *
from app.models.strain_models import *
from app.models.experiment_model import *
from app.models.plate_models import *
from app.model_builders.finders import Finders
class SimpleExperiment():
    """
    creates all DB entities necessary to assembe a simple experiment
    """

    def __init__(self):
        self.experiment = None

    def create(self):

        self._create_concentrations()
        self._create_reagents()
        self.experiment = self._create_experiment()
        return self.experiment

    #-----------------------------------------------------------------------
    # Private below.
    #-----------------------------------------------------------------------


    def _create_concentrations(self):
        for denom, numerator, pref_units in (
                (1, 1, 'X'),(0.4,1, 'microM'),(50,1,'X'),(5,1,'X')):
            Concentration.make(numerator / float(denom), pref_units)

    def _create_reagents(self):
        finder = Finders()
        Reagent.make('DNA Free Water', '22884100', finder._conc_rat(1, 1, 'X'))
        for organism_name, primer_name, role, gene_name in (
        ('Eco', 'Eco63', 'fwd', 'uidA'), ('Eco', 'Eco60', 'rev', 'uidA'),
        ('Eco', 'Eco64', 'fwd', 'uidA'), ('Eco', 'Eco66', 'rev', 'uidA')):
            Primer.make(finder._org(organism_name), primer_name, role, finder._gene(gene_name))
            Reagent.make(primer_name, '-', finder._conc_rat(1, 0.4, 'microM'))


    def _create_rules(self):
        finder = Finders()
        data = (((finder._reagent(Reagent.make_hash('Eco64', Concentration.value_from_quotient(1, 0.4))), ('A', 'B', 1, 2))))