"""
python program to process data from various sources
"""
import time
from tqdm import tqdm

import pandas as pd
from geopy.geocoders import Nominatim


def get_geoloc(name: str, locator: Nominatim, attempts=5):
    """
    gets a single geolocation from Nominatim based on name.
    :param name: name of city to be found
    :param locator: Nominatim geolocator
    :param attempts: number of times try and retrieve geolocation from Nominatim
    :return:
    """
    if attempts <= 0:
        return None
    try:
        geoloc = locator.geocode(name + ', Illinois')
        if geoloc:
            return geoloc
        else:
            time.sleep(.5)
            return get_geoloc(name, locator, attempts=attempts-1)
    except TypeError as e:
        print(e)
        pass

def get_IL_geocoords(df: pd.DataFrame, locator: Nominatim, col='name') -> pd.DataFrame:
    """
    designed to iterate over a series of municipalities, and insert a latitude and longitude into the dataframe

    :param df: the dataframe to be modified
    :param locator: a Nominatim geolocator used to find the latitude and longitude of a city or town
    :param col: the column to iterate over
    :return:
    """
    pbar = tqdm(df[col].items(), desc='Obtaining Geographic Coordinates by Municipality')
    try:
        for i, name in pbar:
            pbar.set_postfix_str(f'Obtaining coordinates for {name}, IL')
            geoloc = get_geoloc(name, locator)
            try:
                df.loc[i, ['lat', 'lon']] = [geoloc.latitude, geoloc.longitude]
                time.sleep(.5)  # to avoid ratelimiting from Nominatim
            except AttributeError:
                print(f'Failed to retrieve geo coordinates for {name} from Nominatim')
        return df
    except KeyError:
        print(f'Your dataframe does not contain the "{col}" column')


def get_IL_df(df: pd.DataFrame, years=5, columns=['ObjectID', 'Status',
                                         'ObsDate', 'DateEnt', 'DateUp',
                                         'Location', 'Latitude', 'Longitude',
                                         'InfestAcre', 'Density', 'Habitat', 'Verified']) -> pd.DataFrame:
    """
    Take a dataframe of recorded Tree of Heaven observations and returns all positive rows that are in Illinois.
    :param df: Dataframe of invasive species data. obtained from www.eddmaps.org
    :param years: number of years to go back from current date (the idea being to not have old, outdated data.)
    :param columns: desired columns to return
    :return IL_df: new dataframe of relevant information in Illinois
    """
    df = df[columns].copy()
    df['DateUp'] = pd.to_datetime(df['DateUp'], format='%m-%d-%y', errors='coerce')
    IL_df = df[(df['Location'].str.contains('Illinois'))
               & (df['Status'] == 'Positive')
               & (df['Verified'] == 'Verified')
               & (df['DateUp'] >= pd.Timestamp.now() - pd.DateOffset(years=years))].copy()
    IL_df.drop(columns=['Status', 'Verified'], inplace=True)
    return IL_df


if __name__ == '__main__':
    locator = Nominatim(user_agent='info_pls')

    # processing city data
    cdf = pd.read_csv('data/orig_city_data.csv').rename(columns={'Name': 'name',
                                                                 'Type': 'type',
                                                                 'Population 2020': 'pop_2020',
                                                                 'Land area sq mi': 'LA_sqmi'})
    cdf['Population density'] = cdf['Population density'].astype(str).str.replace(',', '')
    cdf[['PD_sqmi', 'PD_km2']] = cdf['Population density'].str.split('/', n=1, expand=True)

    cdf['pop_2020'] = cdf['pop_2020'].str.replace(',', '')
    cdf.drop(columns=['PD_km2', 'Population density', 'Land area km2'], inplace=True)

    cdf = get_IL_geocoords(cdf, locator)  # getting geocoordinates for all cities

    cols = cdf.columns.tolist()  # reordering columns
    cols = cols[:2] + cols[-2:] + cols[2:-2]
    cdf = cdf[cols]

    cdf.set_index('name').to_csv('data/city_data.csv')

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
    rev_df = rev_df.sort_values(by='DateUp', ascending=False).drop_duplicates(subset='ObjectID', keep='first')

    toh_df.set_index('ObjectID', inplace=True)
    rev_df.set_index('ObjectID', inplace=True)

    toh_df.update(rev_df[['Density', 'InfestAcre']])
    toh_df['Location'] = toh_df['Location'].str.replace(', Illinois, United States', '')

    toh_df.to_csv(f'{path}/IL_toh.csv')