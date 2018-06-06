import unittest
from pdb import set_trace as st

from app.model_builders.make_ref_exp import ReferenceExperiment
from app.model_builders.batch_reagent_entry import BatchReagentEntry
from app.model_builders.batch_groups_entry import BatchGroupsEntry
from app.models.reagent_model import ReagentModel
from app.models.reagent_group_model import ReagentGroupDetailsModel

class BatchCreatorTest(unittest.TestCase):

    # NOTE using class-level set up, not test method-level.
    @classmethod
    def setUpClass(cls):
        experiment = ReferenceExperiment()
        experiment.create()

    def test_add_some_reagents_with_no_duplicates_present(self):
        submitter = BatchReagentEntry()
        reagents = (
            ('reagent_1', 'category_A','null'),
            ('reagent_2', 'category_A','null'),
            ('reagent_3', 'category_B','null'),
        )
        next_index = len(list(ReagentModel.objects.all()))
        submitter.load_db(reagents)

        saved_reagents = ReagentModel.objects.all()
        self.assertEqual(
            saved_reagents[next_index + 2].name, 'reagent_3')
        self.assertEqual(
            saved_reagents[next_index + 2].category.name, 'category_B')

    def test_make_some_groups(self):
        # Use reagents and units that have been created by the reference
        # experiment.
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

        group_records = ReagentGroupDetailsModel.objects.filter(reagent_group='Pool_43')
        group_records = list(group_records)

        self.assertEqual(group_records[0].reagent_group.group_name, 'Pool_43')
        self.assertEqual(group_records[0].reagent.name, '(Eco)-ATCC-BAA-9999')
        self.assertEqual(group_records[0].concentration, 4)
        self.assertEqual(group_records[0].units.abbrev, 'x')
        
