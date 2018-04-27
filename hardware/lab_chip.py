
import pandas as pd
from hardware.plates import sanitize_well_name


class LabChip:
    """
    Class for LabChip data.

    Attributes:
        lab_chip_files: a dictionary keyed by one of the following
            ['peak', 'raw', 'well'] and valued by the path to the respective
            files.
        well_names: a list of appropriate well names.

    """

    def __init__(self, peak_file, raw_file, well_file):
        """
        Args:
            peak_file: path to a LabChip peak file
            raw_file: path to a LabChip raw file
            well_file: path to a LabChip well file
        """
        super(LabChip, self).__init__()

        self.lab_chip_files = {'peak': peak_file,
                               'raw': raw_file,
                               'well': well_file}

        self.well_names = self.get_well_names()

    def get_well_names(self):
        """
        Helper function to get valid well names.

        Returns:
            well_names: a sorted list of well names
        """
        df = self._get_peak_dataframe()
        well_names = sorted(
            set([n for n in df.index.unique()]))
        well_names = [w for w in well_names if 'ladder' not in w.lower()]

        return well_names

    def get_dataframes(self):
        """
        Generate a dictionary keyed by one of the following
            ['peak', 'raw', 'well'] and valued by the associated DataFrame

        Returns:
            dataframes: a dictionary keyed by one of the following
            ['peak', 'raw', 'well'] and valued by the associated DataFrame
        """

        dataframes = {}
        for f in self.lab_chip_files:
            if f == 'peak':
                dataframes[f] = self._get_peak_dataframe()
            elif f == 'raw':
                dataframes[f] = self._get_raw_dataframe()
            elif f == 'well':
                dataframes[f] = self._get_well_dataframe()

        return dataframes

    def get_data_by_well(self):
        """
        Generate a dictionary keyed by well and valued by all the data
        contained with in the "lab_chip_files"

        Returns:
            a dictionary keyed by well, subkeyed by ['peak', 'raw', 'well'] and
            valued by all the data contained with in the associated
            "lab_chip_files"
        """

        peak_dict = self._get_peak_dictionary()
        raw_dict = self._get_raw_dictionary()
        well_dict = self._get_well_dictionary()

        data_by_well = {}
        for well in self.well_names:
            data_by_well[well] = {'peak': peak_dict[well],
                                  'raw': raw_dict[well],
                                  'well': well_dict[well]}

        return data_by_well

    def _get_peak_dataframe(self):
        """
        Helper function that creates a dataframe from the peak_file.

        Returns:
            df: DataFrame of peak_file
        """
        df = pd.read_csv(self.lab_chip_files['peak'], index_col=1)
        df.index.names = [i.lower().replace(' ', '_') for i in df.index.names]
        df.index = [sanitize_well_name(n) for n in df.index]
        # Need to replace "." in column names as this is incompatable with
        # MongoDB
        df.columns = [c.lower().replace(' ', '_').replace('.', '') for
                      c in df.columns]

        return df

    def _get_raw_dataframe(self):
        """
        Helper function that creates a dataframe from the raw_file.

        Returns:
            df: DataFrame of raw_file
        """
        df = pd.read_csv(self.lab_chip_files['raw'], index_col=0, dtype=float,
                         na_values=' ', keep_default_na=True)
        df.index.names = [i.lower().replace(' ', '_') for i in df.index.names]
        df.columns = [sanitize_well_name(n) for n in df.columns]

        return df

    def _get_well_dataframe(self):
        """
        Helper function that creates a dataframe from the wells_table.

        Returns:
            df: DataFrame of wells_table
        """
        df = pd.read_csv(self.lab_chip_files['well'], index_col=1)
        df.index.names = [i.lower().replace(' ', '_') for i in df.index.names]
        # Need to replace "." in column names as this is incompatable with
        # MongoDB
        df.columns = [c.lower().replace(' ', '_').replace('.', '') for
                      c in df.columns]

        return df

    def _get_well_dictionary(self):
        """
        Converts a well csv, as produced by the LabChip software, into a
            dictionary keyed by well values.

        Returns:
            wells: a dictionary indexed by well
        """
        df = self._get_well_dataframe()
        wells = df.loc[self.well_names]
        wells['experiment_file_name'] = self.lab_chip_files['well']
        wells = wells.T.to_dict()

        return wells

    def _get_peak_dictionary(self):
        """
        Convert a peaks csv, as produced by the LabChip software, into a
            dictionary keyed by well values.

        Returns:
            peaks: a dictionary indexed by well
        """
        df = self._get_peak_dataframe()

        peaks = {}
        for well in self.well_names:
            subset = self._clean_peak_values(
                df.loc[[well]]).set_index('type', append=True)
            for k, v in subset.T.to_dict().items():
                if k[0] in peaks:
                    peaks[k[0]][k[1]] = v
                else:
                    peaks[k[0]] = {k[1]: v}
            peaks[well]['experiment_file_name'] = self.lab_chip_files['peak']

        return peaks

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

    def _get_raw_dictionary(self):
        """
        Convert a raw csv, as produced by the LabChip software, into a
            dictionary keyed by well values.

        Returns:
            raws: a dictionary indexed by well
        """

        df = self._get_raw_dataframe()
        df = self._sanitize_raw_file_column_names(df)

        raws = {}
        for well in self.well_names:
            raws[well] = {}
            raws[well]['data'] = df[well].dropna().tolist()
            raws[well]['sample_period'] = df[well].dropna().index[-1] / \
                df[well].dropna().shape[0]
            raws[well]['experiment_file_name'] = self.lab_chip_files['raw']

        return raws

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
                    swell = sanitize_well_name(col)
                    columns.append('{}'.format(swell))
                except Exception as e:
                    print(e)
        df.columns = columns

        return df
