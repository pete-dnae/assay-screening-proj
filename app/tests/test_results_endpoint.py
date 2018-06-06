import unittest
from django.test import Client
from app.model_builders.make_test_experiment import make_test_experiment

class ExperimentResultsEndpoint(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        make_test_experiment()

    def test_qpcr_endpoint(self):
        c = Client()
        response = c.get('/api/well-results/?expt=A81_E214'
                         '&plate_id=A81_E214_1_ID&wells=["A03","A07","A11","B03"'
                         ',"B07","B11","C03","C07","C11","D03","D07","D11","E03"'
                         ',"E07","E11","F03","F07","F11","G03","G07","G11","H03"'
                         ',"H07","H11"]')
        data = response.data
        self.assertEquals(response.status_code,200)
        ##TODO pick an element and verify
        json_keys = data.keys()
        self.assertIn('summary_table',json_keys)
        self.assertEquals(len(data['summary_table']),12)
        self.assertIn('master_table',json_keys)
        self.assertEquals(len(data['master_table']), 24)
        self.assertIn('amp_graph',json_keys)
        self.assertEquals(len(data['amp_graph']), 24)
        self.assertIn('melt_graph',json_keys)
        self.assertEquals(len(data['melt_graph']), 24)
        self.assertIn('copy_cnt_graph',json_keys)
        self.assertIn('labchip_peaks', json_keys)
        self.assertEquals(len(data['labchip_peaks'].keys()),24)
