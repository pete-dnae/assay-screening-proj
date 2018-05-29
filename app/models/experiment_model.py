from django.db import models

from app.models.rules_script_model import RulesScriptModel

class ExperimentModel(models.Model):
    """
    The top level object that encapsulate an assay screening experiment.
    Contains an experiment name and an allocation rules script.
    """
    experiment_name = models.CharField(max_length=80,primary_key=True)
    experiment_type = models.CharField(max_length=80,default='vannila')
    # We use a foreign key for the rules script text to make sure that we can
    # offer CRUD operations on a RulesScriptModel independently.
    rules_script = models.ForeignKey(
        RulesScriptModel, related_name='experiment_rule_script', 
        on_delete=models.PROTECT)

    @classmethod
    def make(cls, experiment_name, experiment_type,rules_script):
        exp = ExperimentModel.objects.create(
            experiment_name = experiment_name,
            rules_script = rules_script,
            experiment_type = experiment_type
        )
        exp.save()
        return exp
