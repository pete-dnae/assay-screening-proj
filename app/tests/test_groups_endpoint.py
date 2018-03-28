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
        self.assertEqual(json['members'], 
            ['http://testserver/api/reagents/2/',
            'http://testserver/api/reagents/3/']
        )
        self.assertEqual(json['category'],
            'http://testserver/api/reagent-categories/2/')
        self.assertEqual(json['name'], 'Strain')

    def test_put_group(self):
        client = APIClient()
        post_data = {
            'name': 'new name',
            'category': 'http://testserver/api/reagent-categories/1/',
            'members': ['http://testserver/api/reagents/1/',],
        }
        response = client.put(
            '/api/reagent-groups/1/', post_data, format='json')
        json = response.data
        # Smoke test response.
        self.assertEqual(json['members'], 
            ['http://testserver/api/reagents/1/']
        )

    def test_put_group_incompatible_category_error_response(self):
        client = APIClient()
        # Use a reagent whose category is incompatible with that of the group.
        post_data = {
            'name': 'new name',
            'category': 'http://testserver/api/reagent-categories/2/',
            'members': ['http://testserver/api/reagents/1/',],
        }
        response = client.put(
            '/api/reagent-groups/1/', post_data, format='json')
        json = response.data
        err_report = json['non_field_errors']
        self.assertEqual(err_report, 
            ["Cannot add this reagent <Titanium-Taq> to this " + \
            "group, because its category <Buffer Ingredient> does " + \
            "not match the group's category <Strain>"]
        )

    def test_put_group_duplicate_reagent_error_response(self):
        client = APIClient()
        # Use duplicate reagents.
        post_data = {
            'name': 'new name',
            'category': 'http://testserver/api/reagent-categories/1/',
            'members': [
                'http://testserver/api/reagents/1/', 
                'http://testserver/api/reagents/1/'
             ],
        }
        response = client.put(
            '/api/reagent-groups/1/', post_data, format='json')
        json = response.data
        err_report = json['non_field_errors']
        self.assertEqual(err_report, 
            ['Group members must not include duplicates: <Titanium-Taq>']
        )
