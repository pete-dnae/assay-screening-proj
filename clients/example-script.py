
"""
An example script to show you how to use a python script to query a couple of 
the publicly deployed REST API endpoints..

You can explore (and experiment with) all the *fundamental* endpoints available 
by visiting the web service here directly with a browser:

    http://assay-screening.herokuapp.com/

There are also some important *convenience* endpoints. These are documented 
in:

    docs/convenience-endpoints.md
"""

from clients.utils import get_object


if __name__ == '__main__':

    # Consider making some enquiries about the rules script in the reference
    # experiment in the database...

    experiment = get_object(
        'http://assay-screening.herokuapp.com/api/experiments/1/')

    rules_script = get_object(experiment['rules_script'])

    interp = rules_script['interpretationResults']
    parse_err = interp['parseError']  # If there is a syntax error in script.
    allocation_table = interp['table']  # Otherwise.
    if parse_err:
        print(parse_err)
    else:
        contents_of_well = allocation_table['Plate1']['1']['2']
        print(contents_of_well)
