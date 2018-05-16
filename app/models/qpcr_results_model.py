from django.db import models
from django.contrib.postgres.fields import ArrayField
from .experiment_model import ExperimentModel

class QpcrResultsModel(models.Model):
    """
    This table captures information retrieved from qpcr experiment results
    """

    cycle_threshold = models.FloatField(null=True)
    temperatures = ArrayField(models.FloatField(null=True))
    amplification_cycle = ArrayField(models.FloatField(null=True))
    amplification_delta_rn = ArrayField(models.FloatField(null=True))
    melt_temperature = ArrayField(models.FloatField(null=True))
    melt_derivative = ArrayField(models.FloatField(null=True))
    experiment = models.ForeignKey(ExperimentModel,on_delete=models.PROTECT)
    plate_id = models.CharField(max_length=200)
    well = models.CharField(max_length=100)

    @classmethod
    def make(cls,experiment,plate_id,well, cycle_threshold, temperatures,
             amplification_cycle,amplification_delta_rn, melt_temperature,
             melt_derivative):
        return QpcrResultsModel.objects.create(experiment=experiment,
                                               plate_id=plate_id,
                                               well=well,
                                                cycle_threshold=cycle_threshold
                                               ,temperatures=temperatures,
                                               amplification_cycle=
                                               amplification_cycle,
                                               amplification_delta_rn=
                                               amplification_delta_rn,
                                               melt_temperature=
                                               melt_temperature,
                                               melt_derivative=melt_derivative)
