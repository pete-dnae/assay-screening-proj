from io import BytesIO
import pandas as pd
from hardware.utils import sanitize_well_name


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
        raw_dataframe = self._get_raw_dataframe(data)
        df = self._sanitize_raw_file_column_names(raw_dataframe)
        self.well_names = self._get_well_names(raw_dataframe)
        raws = {}
        for well in self.well_names:
            raws[well] = {}
            raws[well]['data'] = df[well].dropna().tolist()
            raws[well]['sample_period'] = \
                df[well].dropna().index[-1] / df[well].dropna().shape[0]

        return raws

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _get_raw_dataframe(self, data):
        """
        Helper function that creates a dataframe from the raw_file.

        Returns:
            df: DataFrame of raw_file
        """
        bs = BytesIO(data.read())
        df = pd.read_csv(bs,index_col=0, dtype=float,
                         na_values=' ', keep_default_na=True)
        df.index.names = [i.lower().replace(' ', '_') for i in df.index.names]
        df.columns = [sanitize_well_name(n) for n in df.columns]

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
        cols = []
        for col in df.columns.tolist():
            if col.startswith('Ladder'):
                cols.append(col)
            else:
                try:
                    swell = sanitize_well_name(col)
                    cols.append('{}'.format(swell))
                except Exception as e:
                    print(e)
        df.columns = cols

        return df

    def _get_well_names(self, dataframe):
        """
        Helper function to get valid well names.

        Returns:
            well_names: a sorted list of well names
        """

        well_names = sorted(
            set(list(dataframe.columns.values)[1:]))
        well_names = [w for w in well_names if 'ladder' not in w.lower()]

        return well_names
