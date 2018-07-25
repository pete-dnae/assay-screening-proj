
import re
import pandas as pd


PLATE_NAME_HEADER = 'Plate'
PLATE_COL_HEADER = 'Plate Columns'
PRIMER_HEADER = 'Primers'
PA_PRIMER_HEADER = 'PA Primers'
ID_PRIMER_HEADER = 'ID Primers'
TEMPLATE_HEADER = 'Template'
HUMAN_HEADER = 'Human'
VANILLA_ID = [PRIMER_HEADER, TEMPLATE_HEADER, HUMAN_HEADER]
NESTED_IDS = [PA_PRIMER_HEADER, ID_PRIMER_HEADER, TEMPLATE_HEADER,
              HUMAN_HEADER]


def get_user_allocation(excel):
    df = pd.read_excel(excel, sheet_name='allocation')
    df = df.dropna(axis='index', how='all')
    df[PLATE_NAME_HEADER] = df['Plate'].fillna(method='pad')
    df = df.fillna('')
    plates = _extract_plate_data(df)
    return plates


def get_sample_layout(excel, sheet_name):
    df = pd.read_excel(excel, sheet_name=sheet_name, index_col=0)
    layout = {'{}{:02d}'.format(k[0], int(k[1])): _standardize_contents(v)
              for k, v in df.stack().to_dict().items()}
    return layout


def get_id_cols(plate):
    cols = {k for k, v in plate[ID_PRIMER_HEADER].items() if v}
    return tuple(cols)


def get_pa_cols(plate):
    cols = {k for k, v in plate[PA_PRIMER_HEADER].items() if v}
    return tuple(cols)


def _extract_plate_data(df):
    plates = {}
    for plate, grp in df.groupby(PLATE_NAME_HEADER):
        plates[plate] = {k: {} for k in NESTED_IDS}
        for i, row in grp.iterrows():
            cols = _standardize_cols(row[PLATE_COL_HEADER])
            for ni in NESTED_IDS:
                for c in cols:
                    plates[plate][ni][c] = row[ni]
    return plates


def _standardize_cols(cols):
    if isinstance(cols, str) and '+' in cols:
        cols = cols.split('+')
        cols = [int(c.replace(' ', '')) for c in cols]
        return cols
    elif isinstance(cols, (int, float)):
        return [int(cols)]
    else:
        raise ValueError(f'Could not extract out the column values for: {cols}')


def _standardize_contents(label):
    if label == 'NTC':
        return {TEMPLATE_HEADER: '0cp', HUMAN_HEADER: '0ug'}
    else:
        temp, human = _get_template_human_quantities(label)
        return {TEMPLATE_HEADER: temp, HUMAN_HEADER: human}


def _get_template_human_quantities(label):
    temp = re.search('(\d+cp)', label)
    if temp:
        temp = temp.group(1)
    else:
        temp = '0cp'
    human = re.search('(\d+[nu]g) HgDNA', label)
    if human:
        human = human.group(1)
    else:
        human = '0ug'
    return temp, human
