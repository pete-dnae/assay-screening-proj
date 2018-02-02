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
    experiment_name = models.CharField(max_length=80) 
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

