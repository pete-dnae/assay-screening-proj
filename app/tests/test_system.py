from pdb import set_trace as st


from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from app.model_builders.make_ref_exp import ReferenceExperiment

class HighLevelSystemSmokeTest(APITestCase):
    """
    Simple tests that exercise the vast majority of the code to check it runs
    without crashing, and do a few quick and dirty sample-based checks.
    """

    def setUp(self):
        experiment = ReferenceExperiment()
        experiment.create()
        client = APIClient()
        User.objects.create_superuser('admin', 'admin@example.com', 'fabble')
        response = client.post('/auth/obtain_token/', {'username': 'admin',
                                                       'password': 'fabble'})
        self.jwt = response.data['token']
    def test_typical_read_only_use_case(self):
        """
        We'll try to GET the reference experiment from its end point.
        Look up its rules script URL and GET that.
        Then inspect the interpreted rules that come back from the rules script
        endpoint to check that they properly populate some arbitrarily chosen 
        cell.
        This will prove that:
            o  we have built a reference database from the ground up
            o  the models are self-consistent to a large degree
            o  the rules script parser and interpreter sub system is working
            o  the Experiment and RulesScript serialisers are working.
            o  the url / view / serializer plumbing is set up right
        """
        client = APIClient()
        experiment_response = client.get('/api/experiments/Reference '
                                         'Experiment/')
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)
        rules_script_url = experiment_response.data['rules_script']

        rules_script_response = client.get(rules_script_url)
        json = rules_script_response.data
        interp_results = json['interpretationResults']

        # Inspect line number mapping part of response.
        lnums = interp_results['lnums']
        cells = lnums[4]
        self.assertEqual(cells, [(1, 2), (5, 2), (9, 2)])

        # Inspect error report part of response.
        err = interp_results['parseError']
        self.assertIsNone(err)

        # Inspect table allocation part of response.
        table = interp_results['table']
        plate_1 = table['Plate1']
        row = plate_1[1]
        col = row[1]
        self.assertEqual(col, [('Titanium-Taq', 0.02, 'M/uL')])

    def test_put_rules_script_with_error_in_it(self):
        """
        We'll try to PUT to a rules script end point, with a script that has
        a syntax error in it. This will show that the end point provides a
        properly formed response that describes the syntax error.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)
        post_data = {'text': 'I am a malformed rules script'}
        experiment_response = client.get('/api/experiments/Reference '
                                         'Experiment/')
        rules_script_url = experiment_response.data['rules_script']
        resp = client.put(rules_script_url, post_data, format='json')

        message = resp.data['interpretationResults']['parseError']['message']

        self.assertEqual(message, 
            'Line must start with one of the letters V|P|A|T|C. Line 1.')

    def test_allowed_names_end_point(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)
        resp = client.get('/api/allowed-names/', format='json')
        all_names = resp.data

        self.assertEqual(all_names['reagents_and_groups'], [
            '(Eco)-ATCC-BAA-2355',
            '(Eco)-ATCC-BAA-9999',
            'Ec_uidA_6.x_Eco63_Eco60',
            'Efs_cpn60_1.x_Efs04_Efs01',
            'Efs_vanB_1.x_van10_van06',
            'Pool_1',
            'Titanium-Taq'])

        self.assertEqual(all_names['units'], ['%','M/uL','cp','cp/ul',
                                              'dilution','mM','mg/ml','nM',
                                              'ng','ng/ul','uM','ug/ml','x'])

    def test_name_filtered_reagent_query(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)
        # First with a name that does exist.
        resp = client.get('/api/reagents/?name=Titanium-Taq', format='json')
        reagents = resp.data
        self.assertEqual(reagents[0]['name'],
            'Titanium-Taq')

        # Now with a name that does not exist.
        resp = client.get('/api/reagents/?name=fried-rain', format='json')
        reagents = resp.data
        self.assertEqual(len(reagents), 0)
