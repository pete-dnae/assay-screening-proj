from django.db import models

from .odds_and_ends_models import CyclingPattern 
from .reagent_models import MasterMix
from .primer_models import PrimerKit
from .strain_models import StrainKit
from .plate_models import Plate

class Experiment(models.Model):
    """
    The top level object that encapsulate an assay screening experiment.
    Gathers together and qualifies a wide variety of input data, parameters and
    quantities. Also carries the reagent allocation recipes, and will later on
    encapsulate results data. Comprises the apex of a deeply hierarchical 
    data structure. Which under the hood makes references out to steady-state
    stock reagents, and also cumulative company knowledge bases, like the
    primers in play.

    In this first draft, the high level attributes correspond strongly to tabs
    in today's spreadsheets. This modelling should probably be rationalised,
    but it is more important today to get something to offer a promising rival
    to the status quo and to learn lessons from that.
    """
    experiment_name = models.CharField(max_length=80, unique=True) 
    designer_name = models.CharField(max_length=80) 
    pa_mastermix = models.ForeignKey(MasterMix, 
        related_name='experiment_pa', on_delete=models.PROTECT)
    id_mastermix = models.ForeignKey(MasterMix, 
        related_name='experiment_id', on_delete=models.PROTECT)
    primer_kit = models.ForeignKey(PrimerKit, 
        related_name='experiment_primer_kit', on_delete=models.PROTECT)
    strain_kit = models.ForeignKey(StrainKit, 
        related_name='experiment_strain_kit', on_delete=models.PROTECT)
    plates = models.ManyToManyField(Plate)
    pa_cycling = models.ForeignKey(CyclingPattern, 
        related_name='experiment_pa_cycling', on_delete=models.PROTECT)
    id_cycling = models.ForeignKey(CyclingPattern, 
        related_name='experiment_id_cycling', on_delete=models.PROTECT)

    def intelligent_copy(self):
        """
        Knows how to make (and save) a new instance of this model, including
        making a judgement about which attributes (recursively must also be
        replicated, vs which can be left shared).
        """
        # General solution is to set primary key on self to None and then 
        # save() self thus getting a new object with a new primary key. But 
        # in between of course recursively copying the attributes in cases
        # where these must not remain shared between the original and the copy.
        self.pk = None

        self.experiment_name += '_copy'
        self.pa_mastermix = self.pa_mastermix.intelligent_copy()
        self.id_mastermix = self.id_mastermix.intelligent_copy()
        self.primer_kit = self.primer_kit.intelligent_copy()
        self.strain_kit = self.strain_kit.intelligent_copy()

        m2m_intelligent_copy(self.plates)

        self.pa_cycling = self.pa_cycling.intelligent_copy()
        self.id_cycling = self.id_cycling.intelligent_copy()

        return self.save()
