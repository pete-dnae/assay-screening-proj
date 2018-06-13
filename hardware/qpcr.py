
import os
from io import BytesIO
import pandas as pd
import numpy as np
import re
from typing import NewType, Dict, List
from hardware.utils import sanitize_well_name

WellName = NewType('WellName', str)
qPCRInstWell = NewType('qPCRInstWell', Dict)
qPCRInstPlate = Dict[WellName, qPCRInstWell]


class QpcrDataFile:
    """
    A class to hande StepOne Excel files.
    """

    def __init__(self, xls_path=None, verbose=False, file_name=None):
        """
        The common header is parsed from the first sheet.
        All sheets in the file are parsed skipping the header.
        A list of dictionaries is created for storing in the MongoDB, where:
            - each item in the list will be one document in the DB
            - each document is made unique by:
                expt, plate_type, plate_id, well
        """

        self.file_name = os.path.basename(xls_path) if xls_path else file_name
        self.xls_path = xls_path
        self.verbose = verbose
        self.expt = 'UNKNOWN'

    def get_common_header(self, xls):
        """
        The StepOne Excel has a common header with 2 columns on each sheet.
        Parse the header from the first sheet and get the number of rows.
        The number of rows can then be used to skip headers for all sheets.
        """

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

    def get_dataframes(self, data=None):
        """
        Parses all sheets in the excel file and returns a dictionary of
            dataframes:
            - one dataframe for the common header
            - one dataframe per sheet in the Excel file
        """

        # Some files have a sheet called Reagent Information without any data
        exclude_sheets = ['Reagent Information']  # Don't read these sheets
        if self.xls_path:
            if '~$' not in self.xls_path:  # Don't oprocess Excel temporary files
                df_dict = {}  # A dict for a dataframe per sheet
                xls = pd.ExcelFile(self.xls_path)
            # Get the list of
        else:
            df_dict = {}
            bytes = BytesIO(data.read())
            xls = pd.ExcelFile(bytes)

        header_df = self.get_common_header(xls)
        sheets = xls.sheet_names
        sheets = [x for x in sheets if x not in exclude_sheets]
        self.sheet_keys = []
        # Get the common header as a dataframe

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

    def get_data_by_well(self, data=None) -> qPCRInstPlate:
        """
        For all columns in all dataframes, convert columns into dict keys.
        Create a list of dictionaires for easy insertion into MongoDB.
        Null values are replaced with '' to avoid JSON issues downstream.
        """

        docs_by_well = {}

        df_dict = self.get_dataframes(data)
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


def get_ct(qpcr_data: qPCRInstWell):
    """
    Gets the ct value from qPCR data.
    :param qpcr_data: an instance of qPCRInstWell
    :return:
    """
    ct = qpcr_data['results']['results']['ct']
    if ct:
        return ct
    else:
        return None


def get_tm(qpcr_data: qPCRInstWell, tm) -> float:
    """
    Gets a particular tm value from qPCR data.
    :param qpcr_data: an instance of qPCRInstWell
    :param tm: the tm value to extract, usually one of ['tm1', 'tm2', 'tm3',
    'tm4']
    :return:
    """
    if tm in qpcr_data['results']['results']:
        tm = qpcr_data['results']['results'][tm]
        return tm if tm else None



def get_tms(qpcr_data: qPCRInstWell, tms=('tm1', 'tm2', 'tm3', 'tm4')) -> \
        List[float]:
    """
    Gets all tm values from qPCR data.
    :param qpcr_data: an instance of qPCRInstWell
    :param tms: the tms to extract
    :return:
    """
    tms = [get_tm(qpcr_data, tm) for tm in tms]
    return tms


def calc_tm_deltas(qpcr_data: qPCRInstWell, max_conc_mean_tm: float):
    """
    Calculate the tm deltas given the average melting temperature from the
    maximum template concentration wells.

    :param qpcr_data: an instance of `qPCRInstWell`
    :param max_conc_mean_tm: average of the maximum template concentration wells
    melting temperatures
    :return:
    """
    tms = get_tms(qpcr_data)
    tm_delta = [abs(tm - max_conc_mean_tm) for tm in tms]
    return tm_delta


def get_mean_ct(qpcr_datas: List[qPCRInstWell]):
    """
    Gets the mean ct value from a dictionary of WellConstituents
    :param qpcr_datas: a list of qPCRInstWell instances
    :return:
    """
    cts = [get_ct(qpcr) for qpcr in qpcr_datas]
    cts = [ct for ct in cts if not np.isnan(ct)]
    if cts:
        return np.mean(cts)
    else:
        return np.nan


def calc_mean_tm(qpcr_datas: List[qPCRInstWell],
                 tm: str='tm1'):
    """
    Calculate the mean tm for a set of wells and a particular tm value.
    :param qpcr_datas: a list of qPCRInstWell instances
    :param tm: a dictionary `qPCRInstWell` instances
    :return:
    """
    mean_tm = np.mean([get_tm(qpcr, tm) for qpcr in qpcr_datas])
    return mean_tm


def get_amplification_data(qpcr_datas: qPCRInstWell)->Dict:
    """
    Gets the amplification cycle and amplification delta_rn value arrays from a
    dictionary of WellConstituents
    """
    amplification_cycle = qpcr_datas['results']['amplification_data']['cycle']
    amplification_delta_rn = qpcr_datas['results']['amplification_data'][
        'delta_rn']

    return {'amplification_cycle':amplification_cycle,'amplification_delta_rn':
        amplification_delta_rn}


def get_melt_data(qpcr_datas: qPCRInstWell)->Dict:
    """
        Gets the melt temperature and derivative value arrays from a
        dictionary of WellConstituents
    """

    if 'melt_curve_raw_data' in qpcr_datas['results']:
        melt_temperature = qpcr_datas['results']['melt_curve_raw_data'][
            'temperature']
        melt_derivative = qpcr_datas['results']['melt_curve_raw_data'][
            'derivative']
    else:
        melt_temperature = qpcr_datas['results']['melt_region_temperature_' \
                                                   'data']['value']
        melt_derivative = qpcr_datas['results']['melt_region_derivative_' \
                                                   'data']['value']

    return {'melt_temperature':melt_temperature,
            'melt_derivative':melt_derivative}