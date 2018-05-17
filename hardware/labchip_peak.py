import pandas as pd
from re import search
from io import BytesIO
from hardware.utils import sanitize_well_name


class LabChipPeakProcessor:
    """
    Utility class which knows how to process csv file containing labchip peak
    information
    """
    def __init__(self):

        self.well_names = None

    def parse_labchip_peak_data(self, data):

        peak_dataframe = self._get_peak_dataframe(data)
        self.well_names = self._get_well_names(peak_dataframe)

        peaks = {}
        for well in self.well_names:
            subset = self._clean_peak_values(
                peak_dataframe.loc[[well]]).set_index('type', append=True)
            for k, v in subset.T.to_dict().items():
                if k[0] in peaks:
                    peaks[k[0]][k[1]] = v
                else:
                    peaks[k[0]] = {k[1]: v}

        return peaks

    # -----------------------------------------------------------------------
    # Private below.
    # -----------------------------------------------------------------------

    def _get_peak_dataframe(self, data):
        """
        Helper function that creates a dataframe from the peak_file.

        Returns:
            df: DataFrame of peak_file
        """
        bs = BytesIO(data.read())
        df = pd.read_csv(bs, index_col=1)
        df.index.names = [i.lower().replace(' ', '_') for i in
                          df.index.names]
        df.index = [sanitize_well_name(n) for n in df.index]
        # Need to replace "." in column names as this is incompatable with
        # MongoDB
        df.columns = [c.lower().replace(' ', '_').replace('.', '') for
                      c in df.columns]

        return df

    def _clean_peak_values(self, df):
        """
        Remove NaNs and replace with a peak index (i.e. "Peak 4") according
        to BP size.

        Args:
            df: a peaks dataframe

        Returns:
            df: a cleaned peaks dataframe

        TODO: Determine correct peak index: Match LabChip GX Reviewer
            numbering or use our own?
        """
        markers = (df['type'].str.match('LM|UM', na=False))
        unknowns = (df['type'].str.match('\?', na=False))
        peaks = df[~markers & ~unknowns].sort_values('size_[bp]')

        peak_idx = []
        for i, x in peaks.reset_index().iterrows():
            if pd.isnull(x['type']):
                peak_idx.append('Peak {}'.format(i + 1))
            else:
                peak_idx.append(x['type'])
        peaks['type'] = peak_idx

        df = pd.concat([df[markers], peaks])

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
