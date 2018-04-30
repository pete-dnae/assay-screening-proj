
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

from clients.utils import create_allocation_table


if __name__ == '__main__':

    # Consider making some enquiries about the rules script in the reference
    # experiment in the database...

    experiment = '1'
    allocation_table = create_allocation_table(experiment)
    contents_of_well = allocation_table['Plate1']['1']['2']
    print(contents_of_well)
