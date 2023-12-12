# Illinois_network.py

"""
### Authors:
##### Justin Tung:      'https://github.com/JayTongue'
##### Matt Adam-Houser: 'https://github.com/mhouser42'

This file is for the creation of county network
It constructs a network with nodes and edges
outputs three binary files: the NX network, a county handler, and a neighbor handler.

TODO: doctests for get_neighbor_handler, calc_toh_density_coef, add_tree_density?
"""
import time
from tqdm import tqdm
import pickle

import pandas as pd
import numpy as np
import networkx as nx
import osmnx as ox
from collections import Counter
from my_classes import County


def get_lower_and_upper_bounds(df: pd.DataFrame, col_name: str) -> tuple:
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


def construct_nodes(CG: nx.Graph, df: pd.DataFrame) -> dict:
    """
    takes a dataframe of county information, finds geolocation with OSMnx
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

        county = ' County'
        name, pop, pop_dense = row['name'], row['pop'], row['PD_sqmi']
        pbar.set_postfix_str(f'Working on {name}{county}, IL')

        gdf = ox.geocode_to_gdf(f'{name}{county}, IL').iloc[0]
        node = County(name, lat=gdf['lat'], lon=gdf['lon'], geometry=gdf['geometry'],
                      pop=pop, popdense_sqmi=pop_dense, centroid=gdf['geometry'].centroid)

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
    edges = []
    for i, row in edge_df.iterrows():
        src = row.iloc[0]
        tgt = row.iloc[1]
        rel = row.iloc[2]
        weight = row.iloc[3]
        try:
            edge = (handler[src], handler[tgt], {'weight': weight, 'rel': rel})
            edges.append(edge)
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

    """
    neighbor_handle = {}
    for county in handler:
        all_neighbors = []
        for neighbor in handler[county].get_neighbor_objects(CG):
            neighbor = handler[neighbor.name]
            all_neighbors.append(neighbor)
        neighbor_handle[county] = all_neighbors
    return neighbor_handle


def get_toh_totals_by_county(df: pd.DataFrame, handler: dict) -> (dict, int):
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
    """
    toh_df = pd.read_csv(f'data/tree/Il_toh.csv')
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
    Adds regular tree densities to nodes, based on the counties latitude and longitude.
    REFERENCE: https://www.fs.usda.gov/nrs/pubs/rb/rb_nrs113.pdf, pages 5-6
    :param handler: graph handler with county names for keys and the counties themselves as values
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


def set_up(path: str) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame):
    """
    Loads and returns previously constructed csvs from preprocessing into pandas dataframes.
    :param path: folder the csvs are stored in.
    :return: csvs loaded into dataframes.
    """
    county_df = pd.read_csv(f'{path}/counties.csv')  # for nodes
    edge_df = pd.read_csv(f'{path}/county_edges.csv')  # for edges
    f_edge_df = pd.read_csv(f'{path}/county_edges_fast_highways.csv')  # makes edge weight on highways lower, inc spread
    toh_df = pd.read_csv(f'data/tree/Il_toh.csv')

    return county_df, edge_df, f_edge_df, toh_df


def construct_graph_and_handlers(CG: nx.Graph, county_df: pd.DataFrame, edge_df: pd.DataFrame, toh_df: pd.DataFrame) \
        -> (nx.Graph, dict, dict):
    """
    Takes a NetworkX Graph,a pandas dataframe of counties for nodes, a dataframe of connections between the counties for
    edges, and a dataframe of Tree of Heaven information about each county to be inserted into node attributes,
    and constructs a network representing counties in Illinois, and handlers for both counties and neighboring counties.
    :param CG: NetworkX Graph to be added to
    :param county_df: dataframe containing counties and geographic/population information
    :param edge_df: dataframe containing adjacency and interstate connections between counties
    :param toh_df: dataframe of up-to-date ToH sightings by county.
    :return: NetworkX Graph of Illinois counties, handler for counties, handler for neighboring counties of each county
    """
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
    return CG, county_handler, neighbor_handler


def dump_graph_and_handler(CG: nx.Graph, county_handler: pd.DataFrame, neighbor_handler: pd.DataFrame, prefix=None):
    """
    Pickles Illinois network graph, county handler, and neighbor handler.
    :param CG: NetworkX graph
    :param county_handler: handler for nodes of NetworkX graph
    :param neighbor_handler: handler for nodes and nodes connected to them.
    :param prefix: specify to pickle different versions of graphs/handlers
    """
    prefix = '' if prefix is None else prefix
    pickle.dump(CG, open(f'{path}/{prefix}IL_graph.dat', 'wb'))
    pickle.dump(county_handler, open(f'{path}/{prefix}graph_handler_counties.dat', 'wb'))
    pickle.dump(neighbor_handler, open(f'{path}/{prefix}graph_handler_neighbors.dat', 'wb'))


if __name__ == '__main__':
    path = 'data/location'
    county_df, edge_df, f_edge_df, toh_df = set_up(path)

    CG = nx.Graph()
    fCG = nx.Graph()

    CG, county_handler, neighbor_handler = construct_graph_and_handlers(CG, county_df, edge_df, toh_df)
    fCG, f_county_handler, f_neighbor_handler = construct_graph_and_handlers(fCG, county_df, f_edge_df, toh_df)

    # pickling
    dump_graph_and_handler(CG, county_handler, neighbor_handler)
    dump_graph_and_handler(fCG, f_county_handler, f_neighbor_handler, prefix='fast_')

