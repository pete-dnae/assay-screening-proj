import unittest
from app.images.image_maker import ImageMaker
from app.model_builders.make_ref_exp import ReferenceExperiment
from app.models.experiment_model import ExperimentModel

class ImageMakerTest(unittest.TestCase):

    def setUp(self):
        ReferenceExperiment().create()

    def test_image_renderer(self):
        image_maker = ImageMaker(1)
        image_maker.prepare_images()

