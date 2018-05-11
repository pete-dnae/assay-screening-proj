import unittest
from pdb import set_trace as st

from app.model_builders.make_ref_exp import ReferenceExperiment
from app.model_builders.batch_reagent_entry import BatchReagentEntry
from app.model_builders.batch_groups_entry import BatchGroupsEntry
from app.models.reagent_model import ReagentModel
from app.models.reagent_group_model import ReagentGroupModel

class BatchCreatorTest(unittest.TestCase):

    def setUp(self):
        experiment = ReferenceExperiment()
        experiment.create()

    def test_add_some_reagents(self):
        submitter = BatchReagentEntry()
        reagents = (
            ('reagent_1', 'category_A','null'),
            ('reagent_2', 'category_A','null'),
            ('reagent_3', 'category_B','null'),
        )
        submitter.load_db(reagents)
        sample_reagent = ReagentModel.objects.get(name='reagent_2')
        self.assertEqual(sample_reagent.category.name, 'category_A')


    def test_make_some_groups(self):
        # Use reagents created by the reference experiment.
        submitter = BatchGroupsEntry()
        groups = {
            'Pool_42': (
                ('(Eco)-ATCC-BAA-2355',     1.16, 'x'),
                ('(Eco)-ATCC-BAA-9999',     2,    'x'),
            ),
            'Pool_43': (
                ('(Eco)-ATCC-BAA-2355',     3.32, 'x'),
                ('(Eco)-ATCC-BAA-9999',     4,    'x'),
            )
        }
        submitter.load_db(groups)

        group_records = ReagentGroupModel.objects.filter(group_name='Pool_43')
        group_records = list(group_records)

        self.assertEqual(group_records[0].group_name, 'Pool_43')
        self.assertEqual(group_records[0].reagent.name, '(Eco)-ATCC-BAA-2355')
        self.assertEqual(group_records[0].concentration, 3.32)
        self.assertEqual(group_records[0].units.abbrev, 'x')
        
