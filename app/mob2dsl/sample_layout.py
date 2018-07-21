
import os
import json

PATH = os.path.dirname(os.path.abspath(__file__))


def get_sample_layouts():
    with open(os.path.join(PATH, 'sample_layouts.json'), 'r') as fp:
        layouts = json.load(fp)
    return layouts


def get_sample_layout(layout):
    return get_sample_layouts()[layout]
