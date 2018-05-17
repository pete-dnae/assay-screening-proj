import unittest
import os
from django.test import Client


class ExperitmentResultsTest(unittest.TestCase):

    def setUp(self):
      pass


    def test_excel_entry(self):
        c = Client()
        root = os.path.abspath(os.getcwd())
        with open(root + r'/hardware/tests/data/A81_E214_1_ID.xls', 'rb') as \
                file:
            response = c.post('/api/experiment-results',{'file':file,
                                               'fileName':'A81_E214_1_ID'})
            print(response)