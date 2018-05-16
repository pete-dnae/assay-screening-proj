from io import BytesIO
import pandas as pd
from re import search

class LabChipRaw:
    """
    Utility class that parses csv file containing raw data correspondign to lab
    chip experiments
    """
    def __init__(self):
        self.well_names = None

    def parse_labchip_raw_data(self, data):
        """
                Convert a raw csv, as produced by the LabChip software, into a
                    dictionary keyed by well values.

                Returns:
                    raws: a dictionary indexed by well
                """
        raw_dataframe = self._get_raw_dataframe()
        df = self._sanitize_raw_file_column_names(raw_dataframe)

        raws = {}
        for well in self.well_names:
            raws[well] = {}
            raws[well]['data'] = df[well].dropna().tolist()
            raws[well]['sample_period'] = df[well].dropna().index[-1] / \
                                          df[well].dropna().shape[0]

        return raws

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------



    def _sanitize_well_name(well_name):
        """
        Sanitize non-standard well names to a standard nomenclature.
        :param well_name: a potentially non-standard well name i.e. a single alpha
        followed by a SINGLE numeral
        :return:
        """
        searched = search('([a-zA-Z]+)(\d+)', well_name).groups()
        well_name = '{}{:0>2}'.format(searched[0], searched[1])
        return well_name

    def _get_raw_dataframe(self,data):
        """
        Helper function that creates a dataframe from the raw_file.

        Returns:
            df: DataFrame of raw_file
        """
        bytes = BytesIO(data.read())
        df = pd.read_csv(bytes,index_col=0, dtype=float,
                         na_values=' ', keep_default_na=True)
        df = pd.read_csv(self.lab_chip_files['raw'], index_col=0, dtype=float,
                         na_values=' ', keep_default_na=True)
        df.index.names = [i.lower().replace(' ', '_') for i in df.index.names]
        df.columns = [self._sanitize_well_name(n) for n in df.columns]

        return df


    def _sanitize_raw_file_column_names(self, df):
        """
        Ensures all columns have the correct naming convention, e.g.: B02 as
            opposed to B2

        Args:
            df: dataframe generated from LabChip raw file

        Returns:
            df: a cleaned raws dataframe
        """
        columns = []
        for col in df.columns.tolist():
            if col.startswith('Ladder'):
                columns.append(col)
            else:
                try:
                    swell = self._sanitize_well_name(col)
                    columns.append('{}'.format(swell))
                except Exception as e:
                    print(e)
        df.columns = columns

        return df