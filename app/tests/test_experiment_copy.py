from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status


from app.models.experiment_model import Experiment
from app.model_builders.make_ref_exp import ReferenceExperiment

class CopyExperimentTest(APITestCase):
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
        client = APIClient()
        payload = {
            'experiment_name': 'my experiment',
            'designer_name': 'fred',
            'experiment_to_copy': self.experiment.id,
        }
        response = client.post(
            '/api/experiments/', payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Copied experiment should have id of 2
        new_exp = Experiment.objects.get(id=2)

        # Same rule in both eperiments should be different object, but with
        # same content.
        rule_a = self.experiment.plates.all()[
                    0].allocation_instructions.rule_list.rules.all()[0]
        rule_b = new_exp.plates.all()[
                    0].allocation_instructions.rule_list.rules.all()[0]
        self.assertNotEqual(rule_a.id, rule_b.id)
        self.assertEqual(rule_a.display_string(), rule_b.display_string())
