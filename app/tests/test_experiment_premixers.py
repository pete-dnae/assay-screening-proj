from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status


from app.models.experiment_model import Experiment
from app.premixers.experiment_premixer import ExperimentPremixer
from app.rules_engine.alloc_rule_interpreter import AllocRuleInterpreter
from app.rules_engine.rule_script_parser import RuleScriptParser
from app.model_builders.make_ref_exp import ReferenceExperiment
from app.model_builders.common_modules import CommonModules
from app.model_builders.finders import Finders
class IdentifyPremixersTest(APITestCase):
    """
    Check that a POST to the api/experiments end-point sucessfully
    creates and returns a new experiment.

    Also checks that those part of the new experiment that should be newly
    created are, and those parts that should remain as foreign key references
    to shared objects, are also correct.
    """

    def setUp(self):
        self.experiment = ReferenceExperiment().create()


    def test_new_experiment_endpoint(self):
        experiment=Experiment.objects.get(id=1)
        rule_script=experiment.rule_script.script
        alloc_rule_lst=[]
        common_modules = CommonModules()
        parsed_rules = RuleScriptParser(common_modules.reagents,common_modules.units,rule_script).parse()
        for i,plate in parsed_rules.items():
            rule_interpreter = AllocRuleInterpreter(plate)
            interpreted_allocation=rule_interpreter.interpret()
            alloc_rule_lst.append(interpreted_allocation)
        experiment_premixer = ExperimentPremixer(alloc_rule_lst)
        # premixes = experiment_premixer.extract_premixes()
        experiment_premixer.extract_premixes()



