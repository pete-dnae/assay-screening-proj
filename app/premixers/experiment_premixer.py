from collections import Counter
from pdb import set_trace as st
from .premixer import Premixer

class ExperimentPremixer:

    def __init__(self,allocResults):

        self._allocation_results=allocResults
        self._buckets = self._flatten_results(self._allocation_results)

    def extract_premixes(self):
        """
        Function flattens the allocation results object to a array of sets containing hash value of reagents used per
        column in each  set
        Premixer object is then created with the flat array and *find_premixes()* function is called to find premixes for
        the input array.
        """
        premixer = Premixer(self._buckets)
        premixer.find_premixes()
        return premixer.premixes

    # -----------------------------------------------------------------------
    # Private below
    # -----------------------------------------------------------------------

    def _flatten_results(self,allocation_results):
        """
        Function flatens the allocation results dictionary into a single array
        array contains a set per each column ,each set then contains the hash
        value of the reagents present in them
        """
        flat_array=[]
        for result_table in allocation_results:
            for rowkey, row in result_table.rows.items():
                for colkey,column in row.items():
                    flat_array.append(set(column))
        return flat_array

