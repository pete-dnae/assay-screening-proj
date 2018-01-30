from rest_framework.test import APITestCase

from app.model_builders.make_ref_exp import ReferenceExperiment
from app.models.odds_and_ends_models import smart_deep_copy_model

class ModelCopyTest(APITestCase):
    """
    Test that the intelligent copying of model objects recursively works.
    """

    def setUp(self):
        self.experiment = ReferenceExperiment().create()

    def test_experiment_copy(self):
        new_experiment = smart_deep_copy_model(self.experiment)

        # Assert with a few example samples, that the copy contains the same
        # definition as the source, but by referring to fundamentally new
        # objects in the database.

        # The top level id's differ

        # An example that proves that the duplication of foreign keys has worked.

        # An example that proves that the duplication of many to many keys has
        # worked.

        # An example that proves that some model clases can opt-out.
