# Illinois_network.py

"""
This file is for the creation of county network
"""

import time
from tqdm import tqdm
import pickle

import pandas as pd
import networkx as nx
import osmnx as ox
from my_classes import City, County


def construct_nodes(CG: nx.Graph, df: pd.DataFrame, is_county=True):
    """
    takes a dataframe of county information, finds geolocation with OSMnx
    :param is_county: 
    :param CG: graph to be populated
    :param df: dataframe with county information
    :return count_dict: a dictionary to reference nodes by name
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
                          bbox_n=gdf['bbox_north'], bbox_s=gdf['bbox_south'],
                          bbox_e=gdf['bbox_east'], bbox_w=gdf['bbox_west'],
                          pop=pop, popdense_sqmi=pop_dense, centroid=gdf['geometry'].centroid)
        else:
            node = City(name, lat=gdf['lat'], lon=gdf['lon'], geometry=gdf['geometry'],
                        bbox_n=gdf['bbox_north'], bbox_s=gdf['bbox_south'],
                        bbox_e=gdf['bbox_east'], bbox_w=gdf['bbox_west'],
                        pop=pop, popdense_sqmi=pop_dense, centroid=gdf['geometry'].centroid)
        CG.add_node(node)
        handler[name] = node
        count += 1
        if count >= len(df):
            pbar.set_postfix_str('Done!')

        time.sleep(.5)
    return handler


def construct_edges(CG: nx.Graph, edge_df: pd.DataFrame, handler: dict, rel='adjacent'):
    """
    takes a graph with nodes, a dataframe instructions, and a dictionary of nodes
    :param CG:
    :param edge_df:
    :param handler:
    :param rel:
    """
    src_h = handler['C'] if rel == 'adjacent' else handler['c']
    tgt_h = handler['C'] if rel != 'interstate' else handler['c']

    edges = []
    for i, row in edge_df.iterrows():
        src = row.iloc[0]
        tgt = row.iloc[1]
        irel = row.iloc[2]
        weight = row.iloc[3]
        try:
            edge = (src_h[src], tgt_h[tgt], {'weight': weight, 'rel': irel})
            edges.append(edge)  # appending to list as it is more efficient to add all edges at once
        except KeyError as e:
            print(f'Key error: {e}: This node doesn\'t exist in the handler')
    CG.add_edges_from(edges)


if __name__ == '__main__':
    path = 'data/location'
    county_df = pd.read_csv(f'{path}/counties.csv')  # for nodes
    edge_df = pd.read_csv(f'{path}/edges.csv')  # for edges
    city_df = pd.read_csv(f'{path}/target_cities.csv')

    CG = nx.Graph()

    # adding county and city nodes to graph and consolodating handlers
    county_dict = construct_nodes(CG, county_df)
    city_dict = construct_nodes(CG, city_df, is_county=False)
    handler = {'C': county_dict, 'c': city_dict}

    # adding edges
    adjacent_e = edge_df[(edge_df['type'] == 'adjacent') & (edge_df['weight'] == 1)]
    interstate_e = edge_df[(edge_df['type'] == 'interstate') & (edge_df['weight']) == .1]
    constituent_e = edge_df[(edge_df['type'] == 'constituent')]

    construct_edges(CG, adjacent_e, handler)
    construct_edges(CG, interstate_e, handler, rel='interstate')
    construct_edges(CG, constituent_e, handler, rel='constituent')

    # pickling
    pickle.dump(CG, open(f'{path}/IL_graph.dat', 'wb'))
    pickle.dump(handler, open(f'{path}/graph_handler.dat', 'wb'))
