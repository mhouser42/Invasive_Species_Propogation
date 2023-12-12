"""
python program to process data from various sources
"""
import time
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup

import pandas as pd
from geopy.geocoders import Nominatim


def replace_curly_apostrophes_and_strip(value: str, replacements=(('“', '"'),
                                                                  ('”', '"'),
                                                                  ('‘', "'"),
                                                                  ('’', "'"))) -> str:
    """
    Tree of heaven data has wrong kind of quotations around string data. This function handles that by replacing all
    single and double quotation marks with standard used in python

    :param value: value in column to be changed
    :param replacements: tuples of paired quotation marks.
    :return value: returns the cleaned values
    """

    if isinstance(value, str):
        for quote, replacement in replacements:
            value = value.replace(quote, replacement)
        value = value.strip()
    return value


def get_geoloc(name: str, locator: Nominatim, attempts=5):
    """
    gets a single geolocation from Nominatim based on name.
    :param name: name of city or county to be found
    :param locator: Nominatim geolocator
    :param attempts: number of times try and retrieve geolocation from Nominatim
    :return: gets the geolocation of a city or county
    """
    if attempts <= 0:
        return None
    try:
        geoloc = locator.geocode(name + ', Illinois')
        if geoloc:
            return geoloc
        else:
            time.sleep(.5)
            return get_geoloc(name, locator, attempts=attempts - 1)
    except TypeError as e:
        print(e)
        pass


def get_IL_geocoords(df: pd.DataFrame, locator: Nominatim, col='name') -> pd.DataFrame:
    """
    designed to iterate over a series of municipalities, and insert a latitude and longitude into the dataframe

    :param df: the dataframe to be modified
    :param locator: a Nominatim geolocator used to find the latitude and longitude of a city or town
    :param col: the column to iterate over
    :return df: of geocoordinate
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


def get_IL_ToH_df(df: pd.DataFrame, years=5, columns=None) -> pd.DataFrame:
    """
    Take a dataframe of recorded Tree of Heaven observations and returns all positive rows that are in Illinois.
    :param df: Dataframe of invasive species data. obtained from www.eddmaps.org
    :param years: number of years to go back from current date (the idea being to not have old, outdated data.)
    :param columns: desired columns to return
    :return IL_df: new dataframe of relevant information in Illinois
    """
    if columns is None:
        columns = ['ObjectID', 'Status',
                   'ObsDate', 'DateEnt', 'DateUp',
                   'Location', 'Latitude', 'Longitude',
                   'InfestAcre', 'Density', 'Habitat', 'Verified']

    df = df[columns].copy()
    df['DateUp'] = pd.to_datetime(df['DateUp'], format='%m-%d-%y', errors='coerce')
    IL_df = df[(df['Location'].str.contains('Illinois'))
               & (df['Status'] == 'Positive')
               & (df['Verified'] == 'Verified')
               & (df['DateUp'] >= pd.Timestamp.now() - pd.DateOffset(years=years))].copy()
    IL_df.drop(columns=['Status', 'Verified'], inplace=True)
    return IL_df


def handle_counties():
    """
    Scrapes and processes county data from www.usa.com, and saves to a csv.
    """
    request = requests.get(
        'http://www.usa.com/rank/illinois-state--population-density--county-rank.htm?hl=&hlst=&wist=&yr=&dis=&sb=DESC&plow=&phigh=&ps=')
    soup = BeautifulSoup(request.text, 'html.parser')
    data = []
    table = soup.find_all('table')[1]

    change_map = {'Dupage': 'DuPage',
                  'Mchenry': 'McHenry',
                  'Saint Clair': 'St. Clair',
                  'Dekalb': 'DeKalb',
                  'Mclean': 'McLean',
                  'La Salle': 'LaSalle',
                  'Mcdonough': 'McDonough',
                  'Dewitt': 'DeWitt'}

    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        cols = [val.text.strip() for val in cols]
        pop_dense = float(cols[1].replace(',', '').replace('/sq mi', ''))

        county, pop = cols[2].replace(',', '').split('/')
        county = county.replace(' IL', '').strip()
        pop = int(pop)

        if county in change_map:
            county = change_map[county]

        data.append({'name': county, 'pop': pop, 'PD_sqmi': pop_dense})

    pd.DataFrame(data).to_csv('data/location/counties.csv', index=False)


def handle_cities():
    """
    Processes city data by calling Nominatim for each city
    """
    path = 'data/location'
    locator = Nominatim(user_agent='info_pls')
    # processing city data
    cdf = pd.read_csv('data/orig_city_data.csv', encoding='').rename(columns={'Name': 'name',
                                                                              'Type': 'type',
                                                                              'Population 2020': 'pop',
                                                                              'Land area sq mi': 'LA_sqmi'})
    cdf['Population density'] = cdf['Population density'].astype(str).str.replace(',', '')
    cdf[['PD_sqmi', 'PD_km2']] = cdf['Population density'].str.split('/', n=1, expand=True)
    cdf['pop'] = cdf['pop'].str.replace(',', '')
    cdf.drop(columns=['PD_km2', 'Population density', 'Land area km2'], inplace=True)
    cdf = get_IL_geocoords(cdf, locator)  # getting geocoordinates for all cities
    cols = cdf.columns.tolist()  # reordering columns
    cols = cols[:2] + cols[-2:] + cols[2:-2]
    cdf = cdf[cols]
    cdf.set_index('name').to_csv(f'{path}/cities.csv', encoding='latin1')


def handle_string_errors(df: pd.DataFrame) -> pd.DataFrame:
    """
    handles some common name errors in dataframe
    :param df: dataframe to be fixed
    :return df: dataframe with corrected names
    """
    df['county'] = df['county'].str.replace('"', '')
    change_map = {
        'Dupage': 'DuPage',
        'Mchenry': 'McHenry',
        'Saint Clair': 'St. Clair',
        'Dekalb': 'DeKalb',
        'Mclean': 'McLean',
        'La Salle': 'LaSalle',
        'Mcdonough': 'McDonough',
        'De Witt': 'DeWitt'
    }
    df['county'] = df['county'].replace(change_map)
    return df


def calc_infest_index(toh_df: pd.DataFrame, keep_nulls=False) -> pd.DataFrame:
    """
    Indexes the infestation levels by using a density map
    :param toh_df: dataframe of ToH data
    :param keep_nulls: whether the dataframe returns null values
    :return toh_df: pd.DataFrame
    """
    toh_df = toh_df.copy()
    if not keep_nulls:
        toh_df.dropna(subset=['infest_acre', 'density'], inplace=True)
        toh_df = toh_df[(toh_df['infest_acre'] != 0) & (toh_df['density'] != 0)]
    density_mapping = {'<5%': .04,
                       '>25%': .3,
                       '>50%': .55,
                       '5-25%': .15,
                       '25-50%': .375,
                       '50-75%': .625,
                       'High': .625,
                       'Low': .04,
                       'Medium': .375
                       }
    toh_df['density'] = toh_df['density'].map(density_mapping).astype(float)
    toh_df['infest_acre'] = pd.to_numeric(toh_df['infest_acre'])
    toh_df['infest_index'] = toh_df['density'] * toh_df['infest_acre']

    return toh_df


def update_with_revisits(toh_df: pd.DataFrame, rev_df: pd.DataFrame) -> pd.DataFrame:
    """
    Updates the toh_DataFrame with information from rev_df
    to maintain toh_DataFrame currency
    :param toh_df: Dataframe with Tree of Heaven sightings
    :param rev_df: Revisits to sight locations
    :return toh_df: the updated tree of heaven dataframe
    """
    rev_df = rev_df.sort_values(by='DateUp',
                                ascending=False).drop_duplicates(subset='ObjectID',
                                                                 keep='first')
    toh_df.set_index('ObjectID', inplace=True)
    rev_df.set_index('ObjectID', inplace=True)
    toh_df.update(rev_df[['Density', 'InfestAcre']])
    toh_df['Location'] = toh_df['Location'].str.replace(', Illinois, United States', '')
    return toh_df


def handle_toh():
    """
    processes Tree of Heaven data
    renames and establishes columns
    Saves to CSV
    """

    path = 'data/tree'
    toh_df = get_IL_ToH_df(pd.read_csv(f'{path}/mappings.csv', encoding='latin-1',
                                       low_memory=False).rename(columns={'objectid': 'ObjectID'}))
    rev_df = get_IL_ToH_df(pd.read_csv(f'{path}/revisits.csv', encoding='latin-1'),
                           columns=['ObjectID', 'Status',
                                    'DateEnt', 'DateUp',
                                    'Location', 'Latitude', 'Longitude',
                                    'InfestAcre', 'Density', 'Verified'])
    # handling duplicates in rev_df
    toh_df = update_with_revisits(toh_df, rev_df)
    # changing names and saving to csv
    toh_df.reset_index(inplace=True)
    toh_df.rename(columns={'ObjectID': 'id', 'ObsDate': 'obs_date', 'DateEnt': 'ent_date', 'DateUp': 'date_up',
                           'Location': 'county', 'Latitude': 'lat', 'Longitude': 'lon',
                           'InfestAcre': 'infest_acre', 'Density': 'density', 'Habitat': 'habitat'
                           }, inplace=True)

    toh_df = handle_string_errors(toh_df)
    toh_df = calc_infest_index(toh_df)

    toh_df.set_index('id', inplace=True)
    toh_df.to_csv(f'{path}/IL_toh.csv')


if __name__ == '__main__':
    handle_counties()
    # handle_cities()
    handle_toh()
