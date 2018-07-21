
import os
import json

PATH = os.path.dirname(os.path.abspath(__file__))


def get_mastermixes():
    with open(os.path.join(PATH, 'mastermix.json'), 'r') as fp:
        layouts = json.load(fp)
    return layouts


def get_mastermix(mastermix):
    return get_mastermixes()[mastermix]
