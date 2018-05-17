from django.db import models
from app.models.qpcr_results_model import QpcrResultsModel
class LabChipResults(models.Model):
    """
    Model captures information retrieved from labchip experiment results
    """
    labchip_well = models.CharField(max_length=100)
    peak_name = models.CharField(max_length=100)
    size =  models.FloatField(null=True)
    concentration = models.FloatField(null=True)
    molarity = models.FloatField(null=True)
    qpcr_well = models.ForeignKey(QpcrResultsModel,on_delete=models.PROTECT)

    @classmethod
    def make(cls, labchip_well,peak_name,size,concentration,molarity,qpcr_well):
        return LabChipResults.objects.create(labchip_well=labchip_well,
                                             peak_name=peak_name,
                                             size=size,
                                             concentration=concentration,
                                             molarity=molarity,
                                             qpcr_well=qpcr_well)


