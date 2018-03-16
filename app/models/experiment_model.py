from django.db import models

from .odds_and_ends_models import CyclingPattern 
from app.models.rule_models import RuleScript

class Experiment(models.Model):
    """
    The top level object that encapsulate an assay screening experiment.
    Contains an experiment name and an allocation rules script.
    """
    experiment_name = models.CharField(max_length=80) 
    # We use a foreign key for the rules script text to make sure that we can
    # offer CRUD operations on a RulesScript independently.
    rules_script = models.ForeignKey(
        RulesScript, related_name='experiment_rule_script', 
        on_delete=models.PROTECT)

    @classmethod
    def make(cls, experiment_name, rules_script):
        exp = Experiment.objects.create(
            experiment_name = experiment_name,
            rules_script = rules_script
        )
        exp.save()
        return exp

    @classmethod
    def clone(cls, src):
        return cls.make(
            src.experiment_name, # Plain copy
            RulesScript.clone(src.rule_script) # New
        )

