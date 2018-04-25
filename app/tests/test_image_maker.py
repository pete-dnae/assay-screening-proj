import unittest
from app.images.image_maker import ImageMaker
from app.model_builders.make_ref_exp import ReferenceExperiment

class ImageMakerTest(unittest.TestCase):

    def setUp(self):
        ReferenceExperiment().create()

    def test_image_renderer(self):
        image_maker = ImageMaker('Reference Experiment')
        err,results = image_maker.make_images()
        self.assertIsNone(err)
        expected_keys=['Plate1','Plate42']
        self.assertEquals([*results.keys()],expected_keys)

