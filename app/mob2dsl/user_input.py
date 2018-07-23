
import re
import pandas as pd


PLATE_NAME_HEADER = 'Plate'
PLATE_COL_HEADER = 'Plate Columns'
PA_PRIMER_HEADER = 'PA Primers'
ID_PRIMER_HEADER = 'ID Primers'
TEMPLATE_HEADER = 'Template'
HUMAN_HEADER = 'Human'
ALLOCATED_IDS = [PA_PRIMER_HEADER, ID_PRIMER_HEADER, TEMPLATE_HEADER,
                 HUMAN_HEADER]


def get_user_allocation(excel):
    df = pd.read_excel(excel, sheet_name='allocation')
    df = df.dropna(axis='index', how='all')
    df[PLATE_NAME_HEADER] = df['Plate'].fillna(method='pad')
    df = df.fillna('')
    plates = _extract_plate_data(df)
    return plates


def get_allocated_cols(plate):
    allocated_cols = set([tuple(v.keys()) for v in plate.values()])
    if len(allocated_cols) == 1:
        return list(allocated_cols)[0]
    else:
        raise ValueError('Values in missing in one of the following: {}'
                         .format(ALLOCATED_IDS))


def get_user_sample_layout(excel):
    df = pd.read_excel(excel, sheet_name='sample layout', index_col=0)
    layout = {'{}{:02d}'.format(k[0], int(k[1])): _standardize_contents(v)
              for k, v in df.stack().to_dict().items()}
    return layout


def _extract_plate_data(df):
    plates = {}
    for plate, grp in df.groupby(PLATE_NAME_HEADER):
        plates[plate] = {k: {} for k in ALLOCATED_IDS}
        for i, row in grp.iterrows():
            cols = row[PLATE_COL_HEADER].split('+')
            cols = [int(c.replace(' ', '')) for c in cols]
            if all(row[ALLOCATED_IDS]):
                for ai in ALLOCATED_IDS:
                    for c in cols:
                        plates[plate][ai][c] = row[ai]
    return plates


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
