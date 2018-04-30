import unittest
from app.images.image_renderer import ImageRenderer


class ImageMakerTest(unittest.TestCase):

    def test_image_renderer(self):

        image_spec = {
            1:{
                1:[('(Eco)-ATCC-BAA-2355', 1.16, 'x')],
                2:[('(Eco)-ATCC-BAA-2355', 1.16, 'x')]
            }
        }
        image_renderer = ImageRenderer(image_spec)
        html_string = image_renderer.make_html()
        table_row_count = html_string.count('<tr>')
        reagent_element = "1.16 x (Eco)-ATCC-BAA-2355"
        reagent_element_count = html_string.count(reagent_element)
        self.assertIn(reagent_element,html_string)
        self.assertEquals(table_row_count,3)
        self.assertEquals(reagent_element_count,2)