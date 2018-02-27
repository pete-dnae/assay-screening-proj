from django.db import models

from .odds_and_ends_models import CyclingPattern 
from app.models.rule_models import RuleScript

class Experiment(models.Model):
    """
    The top level object that encapsulate an assay screening experiment.
    Gathers together and qualifies a wide variety of input data, parameters and
    quantities. Also carries the reagent allocation recipes, and will later on
    encapsulate results data. Comprises the apex of a deeply hierarchical 
    data structure. Which under the hood makes references out to steady-state
    stock reagents, and also cumulative company knowledge bases, like the
    primers in play.
    """
    experiment_name = models.CharField(max_length=80) 
    designer_name = models.CharField(max_length=80)
    rule_script = models.ForeignKey(RuleScript,related_name='experiment_rule_script', on_delete=models.PROTECT)
    pa_cycling = models.ForeignKey(CyclingPattern,
        related_name='experiment_pa_cycling', on_delete=models.PROTECT)
    id_cycling = models.ForeignKey(CyclingPattern, 
        related_name='experiment_id_cycling', on_delete=models.PROTECT)

    @classmethod
    def make(cls, experiment_name, designer_name, rule_script,
            pa_cycling, id_cycling):
        exp = Experiment.objects.create(
            experiment_name = experiment_name,
            designer_name = designer_name,
            rule_script = rule_script,
            pa_cycling = pa_cycling ,
            id_cycling = id_cycling,
        )
        exp.save()
        return exp

    @classmethod
    def clone(cls, src):
        return cls.make(
            src.experiment_name, # Plain copy
            src.designer_name, # Plain copy
            RuleScript.clone(src.rule_script), # New
            CyclingPattern.clone(src.pa_cycling), # New
            CyclingPattern.clone(src.id_cycling) # New
        )

