from pdb import set_trace as st


from rest_framework.test import APIClient
from rest_framework.test import APITestCase


from app.model_builders.make_ref_exp import ReferenceExperiment

class GroupsEndPointTest(APITestCase):
    """
    Tests for the CRUD endpoints for ReagentGroup.
    """

    def setUp(self):
        experiment = ReferenceExperiment()
        experiment.create()

    def test_retrieve_group(self):
        client = APIClient()
        response = client.get('/api/reagent-groups/1/')

        json = response.data
        self.assertEqual(json['group_name'], 'Pool_1')
        self.assertEqual(json['reagent'], 'http://testserver/api/'
                                          'reagents/Efs_cpn60_1.x_Efs04_Efs01/')
        self.assertEqual(json['concentration'], 0.4)
        self.assertEqual(json['units'], 'http://testserver/api/units/3/')

    def test_post_group(self):
        client = APIClient()
        post_data = {
            'group_name': 'new name',
            'reagent': '/api/reagents/Titanium-Taq/',
            'concentration': 0.001,
            'units': '/api/units/1/',
        }
        response = client.post('/api/reagent-groups/', post_data, format='json')
        json = response.data
        # Smoke test response.
        self.assertEqual(json['group_name'], 'new name')

    def test_post_group_error_handling_when_duplicates(self):
        client = APIClient()
        post_data = {
            'group_name': 'new name',
            'reagent': '/api/reagents/Titanium-Taq/',
            'concentration': 0.001,
            'units': '/api/units/1/',
        }
        response = client.post('/api/reagent-groups/', post_data, format='json')
        # This second POST introduces a duplicate  reagent to the group.
        post_data = {
            'group_name': 'new name',
            'reagent': '/api/reagents/Titanium-Taq/',
            'concentration': 0.003,
            'units': '/api/units/2/',
        }
        response = client.post('/api/reagent-groups/', post_data, format='json')
        err_report = response.data['non_field_errors'][0]
        self.assertTrue(err_report.startswith(
            'Cannot add <Titanium-Taq> to group <new name> because it'))
        self.assertTrue(err_report.endswith(
            'already contains it.'))
