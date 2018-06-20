from django.db import models
from .qpcr_results_model import QpcrResultsModel
from .experiment_model import ExperimentModel
class LabChipResultsModel(models.Model):
    """

    Model captures information retrieved from experiment results csv
    file at labchip phase
    Labchip phase happens after a qpcr phase
    Each object contains information about a certain phenomenon(observed peak)
    within a well
    Captures many to one relationship between a labchip well and qpcr well
    """
    labchip_well = models.CharField(max_length=100)
    peak_name = models.CharField(max_length=100)
    size =  models.FloatField(null=True)
    concentration = models.FloatField(null=True)
    purity = models.FloatField(null=True)
    qpcr_well = models.ForeignKey(QpcrResultsModel,on_delete=models.PROTECT)
    experiment = models.ForeignKey(ExperimentModel,on_delete=models.PROTECT)
    labchip_plate_id = models.CharField(max_length=100)

    @classmethod
    def make(cls, experiment,labchip_plate_id,labchip_well,peak_name,purity,
             size,concentration,qpcr_well):
        return LabChipResultsModel.objects.create(labchip_well=labchip_well,
                                             peak_name=peak_name,
                                             size=size,
                                             concentration=concentration,
                                                purity=purity,
                                             qpcr_well=qpcr_well,
                                            experiment=experiment,
                                            labchip_plate_id=labchip_plate_id)


