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
    county_dict = {}
    count = 0

    pbar = tqdm(df.iterrows(), desc='Creating Graph')
    for index, row in pbar:
        name, pop, pop_dense = row['name'], row['pop'], row['PD_sqmi']
        pbar.set_postfix_str(f'Working on {name} {"County" if is_county else ""}, IL')

        gdf = ox.geocode_to_gdf(f'{name} {"County" if is_county else ""}, IL').iloc[0]
        if is_county:
            node = County(name, lat=gdf['lat'], lon=gdf['lon'], geometry=gdf['geometry'],
                          bbox_n=gdf['bbox_north'], bbox_s=gdf['bbox_south'],
                          bbox_e=gdf['bbox_east'], bbox_w=gdf['bbox_west'],
                          pop=pop, popdense_sqmi=pop_dense)
        else:
            node = City(name, lat=gdf['lat'], lon=gdf['lon'], geometry=gdf['geometry'],
                        bbox_n=gdf['bbox_north'], bbox_s=gdf['bbox_south'],
                        bbox_e=gdf['bbox_east'], bbox_w=gdf['bbox_west'],
                        pop=pop, popdense_sqmi=pop_dense)
        CG.add_node(node)
        county_dict[name] = node
        count += 1
        if count >= 102:
            pbar.set_postfix_str('Done!')

        time.sleep(.5)
    return county_dict


def construct_edges(CG: nx.Graph, edge_df: pd.DataFrame, county_dict: dict):
    """
    takes a graph with nodes, a dataframe instructions, and a dictionary of nodes
    :param CG:
    :param edge_df:
    :param county_dict:
    """
    edges = [(county_dict[edge.origin], county_dict[edge.destination]) for edge in edge_df.itertuples(index=False)]
    CG.add_edges_from(edges)


if __name__ == '__main__':
    path = 'data/location'
    ndf = pd.read_csv(f'{path}/counties.csv')  # for nodes
    edf = pd.read_csv(f'{path}/county_edges.csv')  # for edges
    CG = nx.Graph()

    county_dict = construct_nodes(CG, ndf)
    construct_edges(CG, edf, county_dict)

    pickle.dump(CG, open('data/location/IL_graph.dat', 'wb'))
    pickle.dump(county_dict, open('data/location/graph_handler.dat', 'wb'))
