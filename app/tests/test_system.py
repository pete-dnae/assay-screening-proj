from rest_framework.test import APIClient
from rest_framework.test import APITestCase


from app.model_builders.make_ref_exp import ReferenceExperiment
from app.serializers import DetailExperimentSerializer

class HighLevelSystemSmokeTest(APITestCase):
    """
    Simple tests that exercise the vast majority of the code to check it runs
    without crashing, and do a few quick and dirty sample-based checks.
    """

    def setUp(self):
        """
        Reminder - that Django unit tests work on an - in-memory database that
        is created then destroyed before and after tests...

        This setUp step creates a reference experiment in the database, which
        includes building a large number of dependent objects (like Primers for
        example), recursively.

        Observe that this set up step alone excercices most of the model
        code.
        """
        experiment = ReferenceExperiment()
        experiment.create()

    def test_experiment_endpoint(self):
        """
        If we can retreive the reference experiment from its API endpoint and
        it passes even the slightest scrutiny, we have built a reference
        database from the ground up, it shows the models are self-consistent to
        a large degree, and that the ExperimentSerializer is bascically
        working. This will have covered probably 80% of the code just in
        itself.
        """
        client = APIClient()
        response = client.get('/api/experiments/1/')

        # Let's drill down to an arbitrarily chosen rule.
        plate_1 = response.data['plates'][0]
        alloc_instr = plate_1['allocation_instructions']
        rule_list = alloc_instr['rule_list']
        rules = rule_list['rules']
        a_rule = rules[1]
        display_string = a_rule['display_string']

        self.assertEqual(display_string, 
            'Strain, ATCC 700802,Rows:A-H, Cols:4-8')
