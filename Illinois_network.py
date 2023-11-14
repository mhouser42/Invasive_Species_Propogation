# Illinois_network.py

"""
This file is for the creation of county network
"""

import time
from tqdm import tqdm
from typing import Dict

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
from my_classes import Location


def construct_county_nodes(CG: nx.Graph, df: pd.DataFrame):
    """
    takes a dataframe of county information, finds geolocation with OSMnx
    :param CG: graph to be populated
    :param df: dataframe with county information
    :return count_dict: a dictionary to reference nodes by name
    """
    county_dict = {}
    count = 0

    pbar = tqdm(df.iterrows(), desc='Creating Graph')
    for index, row in pbar:
        name, pop, pop_dense = row['name'], row['pop'], row['PD_sqmi']
        pbar.set_postfix_str(f'Working on {name}, IL')

        gdf = ox.geocode_to_gdf(f'{name}, IL').iloc[0]

        node = Location(name, lat=gdf['lat'], lon=gdf['lon'], geo=gdf['geometry'],
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


def populate_edges(CG: nx.Graph, edge_df: pd.DataFrame, county_dict: dict):
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

    county_dict = construct_county_nodes(CG, ndf)
    populate_edges(CG, edf, county_dict)

