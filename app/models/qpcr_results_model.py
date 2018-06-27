from django.db import models
from django.contrib.postgres.fields import ArrayField
from .experiment_model import ExperimentModel

class QpcrResultsModel(models.Model):
    """
    This model captures information retrieved from qpcr experiment results .
    excel file
    Each object contains information about what was observed in a unique
    physical location(well on a plate)
    """
    #TODO: Find out what these fields mean and provide a description

    cycle_threshold = models.FloatField(null=True)
    temperatures = ArrayField(models.FloatField(null=True))
    amplification_cycle = ArrayField(models.FloatField(null=True))
    amplification_delta_rn = ArrayField(models.FloatField(null=True))
    melt_temperature = ArrayField(models.FloatField(null=True))
    melt_derivative = ArrayField(models.FloatField(null=True))
    experiment = models.ForeignKey(ExperimentModel, on_delete=models.PROTECT)
    qpcr_plate_id = models.CharField(max_length=200)
    qpcr_well = models.CharField(max_length=100)
    ##Updated 27/06/2018
    """
    Two new columns to capture exclusion of a qpcr well and comment against a  
    qpcr well
    """
    exclude_well = models.BooleanField(default=False)
    comment = models.CharField(max_length=200,null=True)

    @classmethod
    def make(cls,experiment,qpcr_plate_id,qpcr_well,cycle_threshold, temperatures,
             amplification_cycle,amplification_delta_rn, melt_temperature,
             melt_derivative,exclude_well,comment):
        return QpcrResultsModel.objects.create(experiment=experiment,
                                               qpcr_plate_id=qpcr_plate_id,
                                               qpcr_well=qpcr_well,
                                               cycle_threshold=cycle_threshold,
                                               temperatures=temperatures,
                                               amplification_cycle=
                                               amplification_cycle,
                                               amplification_delta_rn=
                                               amplification_delta_rn,
                                               melt_temperature=
                                               melt_temperature,
                                               melt_derivative=melt_derivative,
                                               exclude_well=exclude_well,
                                               comment=comment)
