# Illinois_network.py

"""
### Authors:
##### Justin Tung:      'https://github.com/JayTongue'
##### Matt Adam-Houser: 'https://github.com/mhouser42'

This file is for the creation of county network

TODO: doctests for get_neighbor_handler, calc_toh_density_coef, add_tree_density
"""
import collections
import time
from tqdm import tqdm
import pickle

import pandas as pd
import numpy as np
import networkx as nx
import osmnx as ox
from collections import Counter
from my_classes import County


def get_lower_and_upper_bounds(df: pd.DataFrame, col_name):
    """
    return the lower and upper bounds of a column's values
    :param df: dataframe to be accessed
    :param col_name: string name of column to retrieve boundaries
    :return: the lower and upper bounds

  >>> data = {'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
    >>> df = pd.DataFrame(data)
    >>> get_lower_and_upper_bounds(df, 'A')
    (-3.5, 14.5)

    >>> empty_df = pd.DataFrame()
    >>> get_lower_and_upper_bounds(empty_df, 'A')  # Empty DataFrame returns None
    Traceback (most recent call last):
    ...
    KeyError: 'A'
    """
    Q1 = np.percentile(df[col_name], 25)
    Q3 = np.percentile(df[col_name], 75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return lower_bound, upper_bound


def construct_nodes(CG: nx.Graph, df: pd.DataFrame, is_county=True):
    """
    takes a dataframe of county information, finds geolocation with OSMnx
    :param is_county: 
    :param CG: graph to be populated
    :param df: dataframe with county information
    :return count_dict: a dictionary to reference nodes by name

    >>> CG = nx.Graph()
    >>> data = {'name': ['Cook', 'Pope'], 'pop': [10000, 20000], 'PD_sqmi': [50, 60]}
    >>> counties_df = pd.DataFrame(data)
    >>> construct_nodes(CG, counties_df)  # doctest: +ELLIPSIS
    {'Cook': <my_classes.County object at ...>, 'Pope': <my_classes.County object at ...>}

    >>> CG = nx.Graph()
    >>> data = {'name': ['Cook', 'Pope'], 'pop': [10000, 20000], 'PD_sqmi': [50]}
    >>> counties_df = pd.DataFrame(data)
    Traceback (most recent call last):
    ...
    ValueError: All arrays must be of the same length
    """
    handler = {}
    count = 0

    pbar = tqdm(df.iterrows(), desc='Assembling Nodes')
    for index, row in pbar:

        county = ' County' if is_county else f', {row["county"]}'
        name, pop, pop_dense = row['name'], row['pop'], row['PD_sqmi']
        pbar.set_postfix_str(f'Working on {name}{county}, IL')

        gdf = ox.geocode_to_gdf(f'{name}{county}, IL').iloc[0]
        if is_county:
            node = County(name, lat=gdf['lat'], lon=gdf['lon'], geometry=gdf['geometry'],
                          pop=pop, popdense_sqmi=pop_dense, centroid=gdf['geometry'].centroid)
        # else:
        #     node = City(name, lat=gdf['lat'], lon=gdf['lon'], geometry=gdf['geometry'],
        #                 pop=pop, popdense_sqmi=pop_dense, centroid=gdf['geometry'].centroid)
        CG.add_node(node)
        handler[name] = node
        count += 1
        if count >= len(df):
            pbar.set_postfix_str('Done!')

        time.sleep(.5)
    return handler


def construct_edges(CG: nx.Graph, edge_df: pd.DataFrame, handler: dict):
    """
    takes a graph with nodes, a dataframe instructions, and a dictionary of nodes
    :param CG:
    :param edge_df:
    :param handler:
    :param rel:

    >>> CG = nx.Graph()
    >>> handler = {'A': object(), 'B': object(), 'C': object()}
    >>> data = {'Source': ['A', 'B'], 'Target': ['B', 'C'], 'Relation': ['adjacent', 'interstate'], 'Weight': [5, 8]}
    >>> edges_df = pd.DataFrame(data)
    >>> construct_edges(CG, edges_df, handler)

    # nothing is outputted, but test shows verifiation of input

    >>> CG = nx.Graph()
    >>> handler = {'A': object(), 'B': object()}
    >>> data = {'Source': ['A', 'B'], 'Target': ['B', 'C'], 'Relation': ['adjacent', 'interstate'], 'Weight': [5, 8]}
    >>> edges_df = pd.DataFrame(data)
    >>> construct_edges(CG, edges_df, handler)
    Key error: 'C': This node doesn't exist in the handler
    """
    # src_h = handler['C'] if rel == 'adjacent' else handler['c']  # code from when we were trying City and County nodes
    # tgt_h = handler['C'] if rel != 'interstate' else handler['c']

    edges = []
    for i, row in edge_df.iterrows():
        src = row.iloc[0]
        tgt = row.iloc[1]
        rel = row.iloc[2]
        weight = row.iloc[3]
        try:
            # edge = (src_h[src], tgt_h[tgt], {'weight': weight, 'rel': irel})  # for city/county handler
            edge = (handler[src], handler[tgt], {'weight': weight, 'rel': rel})
            edges.append(edge)  # appending to list as it is more efficient to add all edges at once
        except KeyError as e:
            print(f'Key error: {e}: This node doesn\'t exist in the handler')
    CG.add_edges_from(edges)


def get_neighbor_handler(CG: nx.Graph, handler: dict) -> dict:
    """
    Ascertains the saturation status of all neighbors for each county instance,
    returns them as a neighbor object
    :param CG: the graph of county network
    :param handler: the graph handler, with county names for keys and the counties themselves for values
    :return neighbor_handle: another handler, with county names for keys and a
    list of neighboring county nodes for values

    # I don't know how to write doctests for this function
    """
    neighbor_handle = {}
    for county in handler:
        all_neighbors = []
        for neighbor in handler[county].get_neighbor_objects(CG):
            neighbor = handler[neighbor.name]
            all_neighbors.append(neighbor)
        neighbor_handle[county] = all_neighbors
    return neighbor_handle


def get_toh_totals_by_county(df, handler):
    """
    calculates the total saturation_index (acreage X density) and number of sightings of tree of heaven for all nodes
    :param df: dataframe to be assessed
    :param handler: graph handler with county names for keys and the counties themselves as values
    :return county_tots, county_counts: the total saturation of tree of heaven by county
    :return county_counts: the number of tree of heaven sightings in a county.

    >>> handler = {'Cole': object(), 'LaSalle': object()}  # Assuming handler is a dictionary with County objects
    >>> data = {'county': ['Cole', 'LaSalle', 'Cole'], 'infest_index': [10, 5, 8]}
    >>> df = pd.DataFrame(data)
    >>> county_tots, county_counts = get_toh_totals_by_county(df, handler)
    >>> county_tots['Cole']  # Checking the total saturation for 'County A'
    18
    >>> county_counts['LaSalle']  # Checking the number of sightings for 'County B'
    1
    >>> county_counts['Wabash']
    0
    """

    county_tots = {key: 0 for key in handler.keys()}
    county_counts = Counter({key: 0 for key in handler.keys()})
    for index, row in df.iterrows():
        county = row['county']
        infest_index = row['infest_index']
        county_counts[county] += 1
        county_tots[county] += infest_index
    return county_tots, county_counts


def calc_toh_density_coef(df: pd.DataFrame, handler: dict, county_tots: dict, county_counts: dict):
    """
    takes  total saturation and sightings and returns relative tree of heaven density for each county in the network,
    capping at 1.0 and bottoming out at 0.0. This is a relative level based on sightings, with outlier being

    :param df: dataframe of tree of heaven data
    :param handler: graph handler with county names as keys and the counties themselves as values
    :param county_tots: total saturation index by county
    :param county_counts: total sightings by county

    # Not sure how to write tests for this func

    """
    lower, upper = get_lower_and_upper_bounds(toh_df, 'infest_index')
    toh_df['infest_index'] = np.clip(toh_df['infest_index'], lower, upper)
    max_infest = max(df['infest_index'])
    min_infest = min(df['infest_index'])

    for name, node in handler.items():
        total = county_tots[name]
        count = county_counts[name]

        avg_infest = total / count if count != 0 else 0
        avg_infest = max(min(avg_infest, max_infest), min_infest)

        node.toh_density = round((avg_infest / max_infest), 2) if max_infest > 0 else 0


def add_tree_density(handler: dict):
    """
    adds regular tree densities to nodes, based on the counties latitude and longitude.
    REFERENCE: https://www.fs.usda.gov/nrs/pubs/rb/rb_nrs113.pdf, pages 5-6
    :param handler: graph handler with county names for keys and the counties themselves as values

    # not sure how to doctest this func
    """
    peoria = handler['Peoria']
    hardin = handler['Hardin']
    clark = handler['Clark']
    for name, county in handler.items():
        if (county.centroid.y <= hardin.centroid.y) or \
                ((county.centroid.y <= peoria.centroid.y) and (county.centroid.x <= peoria.centroid.x)):
            county.tree_density = 0.6
        elif county.centroid.y <= clark.centroid.y:
            county.tree_density = 0.4
        else:
            county.tree_density = 0.2


if __name__ == '__main__':
    path = 'data/location'
    county_df = pd.read_csv(f'{path}/counties.csv')  # for nodes
    edge_df = pd.read_csv(f'{path}/county_edges.csv')  # for edges
    toh_df = pd.read_csv(f'data/tree/Il_toh.csv')
    # city_df = pd.read_csv(f'{path}/target_cities.csv')

    CG = nx.Graph()

    # adding nodes
    county_handler = construct_nodes(CG, county_df)

    # adding edges
    construct_edges(CG, edge_df, county_handler)

    # adding Tree of Heaven and regular tree densities

    county_tots, county_counts = get_toh_totals_by_county(toh_df, county_handler)
    calc_toh_density_coef(toh_df, county_handler, county_tots, county_counts)
    add_tree_density(county_handler)

    # getting a handler of all node neighbors in graph
    neighbor_handler = get_neighbor_handler(CG, county_handler)

    # pickling
    pickle.dump(CG, open(f'{path}/IL_graph.dat', 'wb'))
    pickle.dump(county_handler, open(f'{path}/graph_handler_counties.dat', 'wb'))
    pickle.dump(neighbor_handler, open(f'{path}/graph_handler_neighbors.dat', 'wb'))

    # city_dict = construct_nodes(CG, city_df, is_county=False)
    # handler = {'C': county_dict, 'c': city_dict}

    # adding edges
    # # adjacent_e = edge_df[(edge_df['type'] == 'adjacent') & (edge_df['weight'] == 1)]
    # interstate_e = edge_df[(edge_df['type'] == 'interstate') | (edge_df['weight']) == .1]
    # constituent_e = edge_df[(edge_df['type'] == 'constituent')]
    #
    # construct_edges(CG, adjacent_e, county_dict)
    # construct_edges(CG, interstate_e, county_dict, rel='interstate')
    # construct_edges(CG, constituent_e, handler, rel='constituent')

    # # pickling
    # pickle.dump(CG, open(f'{path}/IL_graph.dat', 'wb'))
    # pickle.dump(CG, open(f'{path}/graph_handler_counties'))
    # pickle.dump(handler, open(f'{path}/graph_handler.dat', 'wb'))
