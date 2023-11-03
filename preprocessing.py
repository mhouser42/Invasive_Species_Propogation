"""
python program to process data from various sources
"""

import pandas as pd


def get_IL_df(df: pd.DataFrame, columns=['ObjectID', 'Status',
                                         'ObsDate', 'DateEnt', 'DateUp',
                                         'Location', 'Latitude', 'Longitude',
                                         'InfestAcre', 'Density', 'Habitat', 'Verified']) -> pd.DataFrame:
    """
    Take a dataframe of recorded Tree of Heaven observations and returns all positive rows that are in Illinois.
    :param df: Dataframe of invasive species data. obtained from www.eddmaps.org
    :param columns: desired columns to return
    :return IL_df: new dataframe of relevant information in Illinois
    """
    df = df[columns]
    IL_df = df[(df['Location'].str.contains('Illinois')) & (df['Status'] == 'Positive')].copy()
    IL_df['Verified'] = IL_df['Verified'] == 'Verified'
    return IL_df


if __name__ == '__main__':
    # processing tree of heaven data
    path = 'data/tree'
    toh_df = get_IL_df(pd.read_csv(f'{path}/mappings.csv', encoding='latin-1',
                                   low_memory=False).rename(columns={'objectid': 'ObjectID'}))
    rev_df = get_IL_df(pd.read_csv(f'{path}/revisits.csv', encoding='latin-1'),
                       columns=['ObjectID', 'Status',
                                'DateEnt', 'DateUp',
                                'Location', 'Latitude', 'Longitude',
                                'InfestAcre', 'Density', 'Verified'])
    # handling duplicates in rev_df
    rev_df['DateUp'] = pd.to_datetime(rev_df['DateUp'], errors='coerce')
    rev_df.set_index('ObjectID', inplace=True)
    rev_df = rev_df.sort_values(by='DateUp', ascending=False)
    rev_df = rev_df.loc[~rev_df.index.duplicated(keep='first')]

    toh_df.set_index('ObjectID', inplace=True)

    toh_df.update(rev_df[rev_df['Verified']][['Density', 'InfestAcre']])
    toh_df.reindex()
    toh_df.to_csv(f'{path}/IL_toh.csv')
