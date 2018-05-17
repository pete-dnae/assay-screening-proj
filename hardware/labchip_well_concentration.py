from io import BytesIO
import pandas as pd


class LabChipWellConcentration:
    """
        Utility class which knows how to process csv file containing labchip
        well concentration and peak count information
        """
    def __init__(self):

        self.well_names = None

    def parse_labchip_concentration_data(self, data):

        concentration_dataframe = self._get_concentration_dataframe(data)
        self.well_names = self._get_well_names(concentration_dataframe)
        wells = concentration_dataframe.loc[self.well_names]
        wells = wells.T.to_dict()

        return wells

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _get_concentration_dataframe(self, data):
        """
        Helper function that creates a dataframe from the wells_table.

        Returns:
            df: DataFrame of wells_table
        """
        bs = BytesIO(data.read())
        df = pd.read_csv(bs, index_col=1)
        df.index.names = [i.lower().replace(' ', '_') for i in df.index.names]
        # Need to replace "." in column names as this is incompatable with
        # MongoDB
        df.columns = [c.lower().replace(' ', '_').replace('.', '') for
                      c in df.columns]

        return df

    def _get_well_names(self, dataframe):
        """
        Helper function to get valid well names.

        Returns:
            well_names: a sorted list of well names
        """

        well_names = sorted(
            set([n for n in dataframe.index.unique()]))
        well_names = [w for w in well_names if 'ladder' not in w.lower()]

        return well_names
