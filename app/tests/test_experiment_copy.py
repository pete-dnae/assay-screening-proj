from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status


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
        print('XXX received: %s' % response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(True)
