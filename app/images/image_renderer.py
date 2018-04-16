from django.template import Context, Template

class ImageRenderer:
    """
    Manufacturer of an html template for the specification provided
    returns a html element as string in response
    """

    def __init__(self,image_spec):

        self.image_spec = image_spec


    def prepare_html_viz(self):
        t = Template("image_template.html")
        image_spec =self.image_spec
        html=t.render(Context(image_spec))
        print(t)