from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status


from app.models.experiment_model import Experiment
from app.models.plate_models import Plate
from app.models.plate_models import AllocationInstructions
from app.models.reagent_models import Reagent
from app.premixers.experiment_premixer import ExperimentPremixer
from app.rules_engine.alloc_rule_interpreter import AllocRuleInterpreter
from app.rules_engine.alloc_rule_interpreter import AllocationResults
from app.model_builders.make_ref_exp import ReferenceExperiment

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
        plates=experiment.plates.all()
        tabulated_result=[]
        for plate in plates:
            alloc_instructions=plate.allocation_instructions
            rules = alloc_instructions.rule_list.rules.all()
            rule_interpreter = AllocRuleInterpreter(rules)
            interpreted_allocation=rule_interpreter.interpret()
            tabulated_result.append(interpreted_allocation)
        experiment_premixer = ExperimentPremixer(tabulated_result)
        premixes = experiment_premixer.extract_premixes()
        self.assertEqual(type(premixes), list)
        element = premixes[0]
        self.assertEqual(type(element), tuple)
        self.assertTupleEqual(element,({'hgDNA:0.000e+00'},[i for i in range(0,192)]))


