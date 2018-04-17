from django.template import Context, Template
from django.template.loader import get_template, render_to_string


class ImageRenderer:
    """
    Manufacturer of an html template for the specification provided
    returns a html element as string in response
    """

    def __init__(self, image_spec):
        self.image_spec = image_spec
        self._rows = None
        self._cols = None
        self._set_row_rol()

    def prepare_html_viz(self):
        return render_to_string('image_template.html',
                                {'image_spec': self.image_spec,
                                 'rows': self._rows, 'cols': self._cols})

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _set_row_rol(self):
        """
        Calculates the max row , col attribute required to draw a complete table
        max col is equal to the number of keys in image_spec as it is keyed by cols
        max row is max key count in row dict, found through recursion on column keys

        Then prepares an array of rows and cols
        """
        _max_col = len(self.image_spec.values())
        _max_row = max(len(v.keys()) for k, v in self.image_spec.items())
        self._cols = [n + 1 for n in range(_max_col)]
        self._rows = [n + 1 for n in range(_max_row)]
