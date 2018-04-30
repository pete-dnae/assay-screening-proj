
import urllib.request
import json


BASE_URL = 'http://assay-screening.herokuapp.com/api/experiments/'


def get_object(url):
    """
    Utility to obtain a python object from the api_path you provide.
    """
    stream = urllib.request.urlopen(url)
    bytes = stream.read()
    encoding = stream.info().get_content_charset('utf-8')
    return json.loads(bytes.decode(encoding))


def create_allocation_table(expt_name: str, base_url=BASE_URL):
    """
    Creates an allocation table (nested dictionary) by querying a base URL
    with an experiment name.

    :param expt_name: name of experiment
    :param base_url: REST endpoint to query against
    :return:
    """

    experiment = get_object('{}{}'.format(base_url, expt_name))
    rules_script = get_object(experiment['rules_script'])
    interp = rules_script['interpretationResults']
    parse_err = interp['parseError']  # If there is a syntax error in script.
    if parse_err:
        raise ValueError(parse_err)
    else:
        allocation_table = interp['table']  # Otherwise.
        return allocation_table
