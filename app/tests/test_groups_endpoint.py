from pdb import set_trace as st


from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from app.model_builders.make_ref_exp import ReferenceExperiment

class GroupsEndPointTest(APITestCase):
    """
    Tests for the CRUD endpoints for ReagentGroup.
    """

    def setUp(self):
        experiment = ReferenceExperiment()
        experiment.create()
        client = APIClient()
        User.objects.create_superuser('admin', 'admin@example.com', 'fabble')
        response = client.post('/auth/obtain_token/', {'username': 'admin',
                                                       'password': 'fabble'})
        self.jwt = response.data['token']



    def test_retrieve_group(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)
        response = client.get('/api/reagent-groups/Pool_1/')

        json = response.data
        self.assertEqual(json['group_name'], 'Pool_1')
        self.assertEqual(json['details'][1]['reagent'],
                         'Efs_cpn60_1.x_Efs04_Efs01')
        self.assertEqual(json['details'][1]['concentration'], 0.4)
        self.assertEqual(json['details'][1]['units'], 'uM')

    def test_post_group(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)
        post_data = {
            'group_name': 'new name',
            'details':[{'reagent': 'Efs_cpn60_1.x_Efs04_Efs01',
            'concentration': 0.001,
            'units': 'uM'}]
        }
        response = client.post('/api/reagent-groups/', post_data, format='json')
        json = response.data
        # Smoke test response.
        self.assertEqual(json['group_name'], 'new name')

    def test_post_group_error_handling_when_duplicates(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)
        post_data = {
            'group_name': 'new name',
            'details':[{'reagent': 'Titanium-Taq',
            'concentration': 0.001,
            'units': 'uM'}]
        }
        response = client.post('/api/reagent-groups/', post_data, format='json')
        # This second POST introduces a duplicate  reagent to the group.
        post_data = {
            'group_name': 'new name',
            'details':[{'reagent': 'Titanium-Taq',
            'concentration': 0.003,
            'units': 'uM'}],
        }
        response = client.post('/api/reagent-groups/', post_data, format='json')
        self.assertTrue(response.status_code,400)
        self.assertTrue(response.status_text,'Bad Request')
