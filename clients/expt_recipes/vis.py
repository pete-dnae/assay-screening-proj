
import pandas as pd


def make_well_contents_frame(well_name, reagents):
    df = pd.DataFrame.from_dict(reagents, orient='columns')
    df.index = [well_name] * len(df.index)
    return df