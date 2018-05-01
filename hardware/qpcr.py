
import os
import pandas as pd
import numpy as np
import re
from typing import NewType, Dict, List

qPCRData = NewType('qPCRData', Dict)

from hardware.plates import WellName, sanitize_well_name


class QpcrDataFile:
    """
    A class to hande StepOne Excel files.
    """

    def __init__(self, xls_path, verbose=False):
        """
        The common header is parsed from the first sheet.
        All sheets in the file are parsed skipping the header.
        A list of dictionaries is created for storing in the MongoDB, where:
            - each item in the list will be one document in the DB
            - each document is made unique by:
                expt, plate_type, plate_id, well
        """

        self.file_name = os.path.basename(xls_path)
        self.xls_path = xls_path
        self.verbose = verbose
        self.expt = 'UNKNOWN'

    def get_common_header(self):
        """
        The StepOne Excel has a common header with 2 columns on each sheet.
        Parse the header from the first sheet and get the number of rows.
        The number of rows can then be used to skip headers for all sheets.
        """
        xls = pd.ExcelFile(self.xls_path)
        df = xls.parse(0, parse_cols=[0, 1], header=None)
        header_rows = df[df[0].isnull()].index[0]
        df = df.head(header_rows).iloc[:, :2]
        df.columns = ['Key', 'Value']  # Rename columns to key and value
        df.set_index('Key', inplace=True)
        inst_type = df[df.index == 'Instrument Type'].Value.values[0].strip()
        if inst_type == 'steponeplus':
            self.plate_type = 'StepOnePlus'
        else:
            self.plate_type = 'StepOneQS{}'.format(inst_type.split()[1])
        return df

    def _stack_step_one_plus_melt(self, input_df):
        """
        Returns a Step One Plus sheet stacked with a columns for Reading &
            Value.
        This is needed for Step One Plus melt point sheets which 1 column
            per reading.
        Sets the attribute plate_type based on the type of isntrument.
        """
        df = input_df.copy()  # To avoid changing the original dataframe
        df = (pd.pivot_table(df, index=['Well', 'Target', 'Reporter Dye'])
              .stack().reset_index())
        df.rename(columns={'level_3': 'Reading', 0: 'Value'}, inplace=True)
        df['Reading'] = [int(x.split()[-1]) for x in df.Reading.values]
        df.sort_values(['Well', 'Reading'], inplace=True)
        return df

    def well_no_to_pos(self, wn, nrows=8, ncols=12):
        """
        Returns the well position for the specified well number.
        Default is a 96-well plate with 8 rows.
        """
        if (wn > 0) and (wn <= (nrows * ncols)):
            row_letter = 'ABCDEFGHIJKLMNOP'
            row = row_letter[int((wn - 1) / ncols)]
            col = ((wn - 1) % ncols) + 1
            well_pos = '%s%02d' % (row, col)
            return well_pos
        else:
            raise ValueError('Cannot convert well number to identifier.')

    def get_dataframes(self):
        """
        Parses all sheets in the excel file and returns a dictionary of
            dataframes:
            - one dataframe for the common header
            - one dataframe per sheet in the Excel file
        """

        # Some files have a sheet called Reagent Information without any data
        exclude_sheets = ['Reagent Information']  # Don't read these sheets
        if '~$' not in self.xls_path:  # Don't oprocess Excel temporary files
            df_dict = {}  # A dict for a dataframe per sheet
            xls = pd.ExcelFile(self.xls_path)
            # Get the list of
            sheets = xls.sheet_names
            sheets = [x for x in sheets if x not in exclude_sheets]
            self.sheet_keys = []
            # Get the common header as a dataframe
            header_df = self.get_common_header()
            if header_df is not None:
                skiprows = len(header_df) + 1
            else:
                raise Exception('Failed to read header.')
            df_dict['header'] = header_df
            # Get the plate ID from the file name
            self.plate_id = '_'.join(self.file_name
                                     .split('_')[:3]).split('.')[0]
            if self.plate_id.count('_') > 1:  # First 2 words are the expt
                self.expt = '_'.join(self.plate_id.split('_')[:2])
            else:
                self.expt = self.plate_id
            for i, sheet in enumerate(sheets):
                sheet_key = sheet.strip().replace(' ', '_').lower()
                self.sheet_keys.append(sheet_key)  # List preserves sheet order
                df = xls.parse(i, skiprows=skiprows)
                if sheet_key == 'amplification_data':
                    self.last_cycle = df.Cycle.max()
                columns_to_sanitise = [x for x in df.columns if
                                       x.startswith('Well')]
                nrows, ncols = (8, 12)

                if (len(columns_to_sanitise) == 1):
                    c0 = columns_to_sanitise[0]

                    if str(sorted(df[c0].unique().tolist())[-1]) == '384':
                        nrows, ncols = (16, 24)

                    if df[c0].dtype in (int, np.int64):
                        df[c0] = \
                            [self.well_no_to_pos(x, nrows=nrows, ncols=ncols)
                             for x in df[c0]]
                for well_col in columns_to_sanitise:
                    # Some sheets have leading blanks on the Well Position
                    first_well = str(df[well_col].values[0]).replace(' ', '')
                    if re.search('[A-Z]', first_well[0]):
                        df[well_col] = df[well_col].str.replace(' ', '')
                        df[well_col] = [sanitize_well_name(x)
                                        for x in df[well_col].values]
                    else:  # It is Well column with integer values delete it
                        df.drop(well_col, axis=1, inplace=True)
                # Rename Well Position to Well
                columns_to_rename = [x for x in df.columns if
                                     x.startswith('Well ')]
                # Don't rename if more than one column needs to be renamed
                # (unexpected columns)
                if len(columns_to_rename) == 1:
                    df.rename(columns={columns_to_rename[0]: 'Well'},
                              inplace=True)
                elif len(columns_to_rename) > 1:
                    print('WARNING: More that one well'
                          ' column to rename ({} | {})'
                          .format(sheet, columns_to_rename))
                if sheet_key == 'results':
                    self.valid_wells = df[df['Sample Name']
                                          .notnull()].Well.values
                # Step One Plus melt sheets contain data that needs transposing
                if self.plate_type.count('Plus') and sheet.startswith('Melt'):
                    df = self._stack_step_one_plus_melt(df)
                # Rename greek delta-Rn to Delat Rn same as QS5/7
                if (self.plate_type.count('Plus') and
                        (sheet == 'Amplification Data')):
                    df.rename(columns={'ΔRn': 'Delta Rn'}, inplace=True)
                # Replace spaces in column names
                for x in df.columns:
                    if x.count(' ') or x.count('Cт') or x.count('CT'):
                        new_name = (x.replace(' ', '_')
                                    .replace('Cт', 'Ct')
                                    .replace('CT', 'Ct'))
                        df.rename(columns={x: new_name}, inplace=True)
                for x in [col for col in df.columns if col.count('Ct')]:
                    try:
                        df.loc[df[x] == 'Undetermined', x] = None
                    except TypeError:
                        pass
                # Make all columns lower case.
                # After above changes to avoid accidental matching above.
                for x in df.columns:
                    df.rename(columns={x: x.lower()}, inplace=True)
                if self.verbose:
                    print('Processed sheet:', sheet)
                df.set_index('well', inplace=True)
                df_dict[sheet_key] = df
            # Remove cycles greater than last cycle from all sheets
            # Needs to be done after all sheets are read since last_cycle
            # is not known in early sheets
            for key in df_dict.keys():
                if key == 'header':
                    continue
                df = df_dict[key]
                if 'cycle' in df.columns:
                    df = df[df.cycle <= self.last_cycle]
                # Remove empty wells
                df_dict[key] = df[df.index.isin(self.valid_wells)]
            return df_dict

    def get_data_by_well(self) -> Dict[WellName, qPCRData]:
        """
        For all columns in all dataframes, convert columns into dict keys.
        Create a list of dictionaires for easy insertion into MongoDB.
        Null values are replaced with '' to avoid JSON issues downstream.
        """

        docs_by_well = {}

        df_dict = self.get_dataframes()
        # Get the common header as a dictionary
        header_df = df_dict['header'].copy().replace(np.nan, '')['Value']

        # Replace any "."s in field names to comply with mongo rules
        header_df.index = [i.replace('.', '*') for i in header_df.index]
        header_dict = header_df.to_dict()

        # Process in order of Workbook
        for i, sheet in enumerate(self.sheet_keys):
            df = df_dict[sheet].copy().replace(np.nan, '')
            grouped = df.groupby(df.index)
            for well, group in grouped:
                if i == 0:
                    # Initialise a dict with keys that make the well ID unique
                    docs_by_well[well] = {
                        'expt': self.expt,
                        'plate_type': self.plate_type,
                        'plate_id': self.plate_id,
                        'well': well,
                    }
                    # Add header results
                    docs_by_well[well]['results'] = {'header':
                                                     header_dict.copy()}

                # Replace any "."s in field names to comply with mongo rules
                group.columns = [c.replace('.', '*') for c in group.columns]

                if group.shape[0] == 1:
                    docs_by_well[well]['results'][sheet] = \
                        group.to_dict(orient='records')[0]
                else:
                    docs_by_well[well]['results'][sheet] = \
                        group.to_dict(orient='list')
                docs_by_well[well] = docs_by_well[well].copy()

        return docs_by_well


def get_ct(qpcr_data: qPCRData):
    """
    Gets the ct value from qPCR data.
    :param qpcr_data: an instance of qPCRData
    :return:
    """
    ct = qpcr_data['results']['results']['ct']
    if ct:
        return ct
    else:
        return np.nan


def get_tm(qpcr_data: qPCRData, tm) -> float:
    """
    Gets a particular tm value from qPCR data.
    :param qpcr_data: an instance of qPCRData
    :param tm: the tm value to extract, usually one of ['tm1', 'tm2', 'tm3',
    'tm4']
    :return:
    """
    tm = qpcr_data['results']['results'][tm]
    if tm:
        return tm
    else:
        return np.nan


def get_tms(qpcr_data: qPCRData, tms=('tm1', 'tm2', 'tm3', 'tm4')) -> \
        List[float]:
    """
    Gets all tm values from qPCR data.
    :param qpcr_data: an instance of qPCRData
    :param tms: the tms to extract
    :return:
    """
    tms = [get_tm(qpcr_data, tm) for tm in tms]
    return tms

