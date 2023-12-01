"""
TODO: write doctests
"""

import pickle

import networkx as nx
from numpy import random
import pandas as pd
from my_classes import MonthQueue


def saturation_main(run_mode: str, iterations: int, use_methods=False) -> pd.DataFrame:
    """
    Main Function that sequences the order of events when running this file
    :param use_methods: a Boolean that decided if saturation is affected by class methods.
    :param run_mode: version of Monte Carlo to run
    :param iterations: number of times to run Monte Carlo
    :return : pandas dataframe of cumulative years
    """
    CG, schema, neighbor_schema = set_up()
    schema = set_coefficients(schema)
    cumulative_df = iterate_through_years(CG, schema, neighbor_schema, iterations, run_mode, use_methods=use_methods)
    return cumulative_df


def set_up() -> (nx.Graph, dict, dict):
    """
    return input files created by the illinois_network.py
    :return CG: Picked graph from illinois_network.py
    :return schema: a dict containing each county and its own class instance
    :return neighbor_schema: a dict containing each county and references the instances of adjacent counties
    """
    path = 'data/location'
    CG = pickle.load(open(f'{path}/IL_graph.dat', 'rb'))
    schema = pickle.load(open(f'{path}/graph_handler_counties.dat', 'rb'))
    neighbor_schema = pickle.load(open(f'{path}/graph_handler_neighbors.dat', 'rb'))
    return CG, schema, neighbor_schema


def set_coefficients(schema: dict) -> dict:
    """
    Sets coefficients for the class attributes
    Changes the attributes within the schema
    :param schema: handler for dictionary
    :return: handler but updated
    """

    coef_dict = {
        'Cook': {'saturation': 0.3, 'egg_count': 105},
        'DuPage': {'saturation': 0.0, 'egg_count': 0},
        'Kane': {'saturation': 0.1, 'egg_count': 20},
        'Will': {'saturation': 0.0, 'egg_count': 0},
        'Winnebago': {'saturation': 0.0, 'egg_count': 0},
        'Lake': {'saturation': 0.0, 'egg_count': 0},
        'McHenry': {'saturation': 0.0, 'egg_count': 0},
        'St. Clair': {'saturation': 0.0, 'egg_count': 0},
        'Kendall': {'saturation': 0.0, 'egg_count': 0},
        'Madison': {'saturation': 0.0, 'egg_count': 0},
        'Rock Island': {'saturation': 0.0, 'egg_count': 0},
        'Peoria': {'saturation': 0.0, 'egg_count': 0},
        'Sangamon': {'saturation': 0.0, 'egg_count': 0},
        'Tazewell': {'saturation': 0.0, 'egg_count': 0},
        'Champaign': {'saturation': 0.2, 'egg_count': 100},
        'Boone': {'saturation': 0.0, 'egg_count': 0},
        'Macon': {'saturation': 0.0, 'egg_count': 0},
        'Kankakee': {'saturation': 0.0, 'egg_count': 0},
        'DeKalb': {'saturation': 0.0, 'egg_count': 0},
        'Williamson': {'saturation': 0.0, 'egg_count': 0},
        'McLean': {'saturation': 0.0, 'egg_count': 0},
        'Grundy': {'saturation': 0.0, 'egg_count': 0},
        'Coles': {'saturation': 0.0, 'egg_count': 0},
        'Jackson': {'saturation': 0.0, 'egg_count': 0},
        'LaSalle': {'saturation': 0.0, 'egg_count': 0},
        'Franklin': {'saturation': 0.0, 'egg_count': 0},
        'Vermilion': {'saturation': 0.0, 'egg_count': 0},
        'Monroe': {'saturation': 0.0, 'egg_count': 0},
        'Stephenson': {'saturation': 0.0, 'egg_count': 0},
        'Whiteside': {'saturation': 0.0, 'egg_count': 0},
        'Adams': {'saturation': 0.0, 'egg_count': 0},
        'Clinton': {'saturation': 0.0, 'egg_count': 0},
        'Knox': {'saturation': 0.0, 'egg_count': 0},
        'Woodford': {'saturation': 0.0, 'egg_count': 0},
        'Effingham': {'saturation': 0.0, 'egg_count': 0},
        'Ogle': {'saturation': 0.0, 'egg_count': 0},
        'Marion': {'saturation': 0.0, 'egg_count': 0},
        'Jefferson': {'saturation': 0.0, 'egg_count': 0},
        'Saline': {'saturation': 0.0, 'egg_count': 0},
        'Massac': {'saturation': 0.0, 'egg_count': 0},
        'Morgan': {'saturation': 0.0, 'egg_count': 0},
        'Henry': {'saturation': 0.8, 'egg_count': 0},
        'Jersey': {'saturation': 0.0, 'egg_count': 0},
        'Randolph': {'saturation': 0.0, 'egg_count': 0},
        'McDonough': {'saturation': 0.0, 'egg_count': 0},
        'Macoupin': {'saturation': 0.0, 'egg_count': 0},
        'Wabash': {'saturation': 0.0, 'egg_count': 0},
        'Perry': {'saturation': 0.0, 'egg_count': 0},
        'Logan': {'saturation': 0.0, 'egg_count': 0},
        'Lee': {'saturation': 0.0, 'egg_count': 0},
        'Christian': {'saturation': 0.0, 'egg_count': 0},
        'Douglas': {'saturation': 0.0, 'egg_count': 0},
        'Bond': {'saturation': 0.0, 'egg_count': 0},
        'Lawrence': {'saturation': 0.0, 'egg_count': 0},
        'Richland': {'saturation': 0.0, 'egg_count': 0},
        'Crawford': {'saturation': 0.0, 'egg_count': 0},
        'Moultrie': {'saturation': 0.0, 'egg_count': 0},
        'Montgomery': {'saturation': 0.0, 'egg_count': 0},
        'Union': {'saturation': 0.0, 'egg_count': 55},
        'Fulton': {'saturation': 0.0, 'egg_count': 0},
        'DeWitt': {'saturation': 0.0, 'egg_count': 0},
        'Menard': {'saturation': 0.0, 'egg_count': 0},
        'Bureau': {'saturation': 0.0, 'egg_count': 0},
        'Piatt': {'saturation': 0.0, 'egg_count': 0},
        'Livingston': {'saturation': 0.0, 'egg_count': 0},
        'Johnson': {'saturation': 0.0, 'egg_count': 0},
        'Jo Daviess': {'saturation': 0.0, 'egg_count': 0},
        'Cass': {'saturation': 0.0, 'egg_count': 0},
        'Putnam': {'saturation': 0.0, 'egg_count': 0},
        'Warren': {'saturation': 0.0, 'egg_count': 0},
        'Carroll': {'saturation': 0.0, 'egg_count': 0},
        'Clark': {'saturation': 0.0, 'egg_count': 0},
        'Cumberland': {'saturation': 0.0, 'egg_count': 0},
        'Alexander': {'saturation': 0.0, 'egg_count': 0},
        'Marshall': {'saturation': 0.0, 'egg_count': 0},
        'Fayette': {'saturation': 0.0, 'egg_count': 0},
        'Edwards': {'saturation': 0.0, 'egg_count': 0},
        'Pulaski': {'saturation': 0.0, 'egg_count': 0},
        'Clay': {'saturation': 0.0, 'egg_count': 0},
        'Edgar': {'saturation': 0.0, 'egg_count': 0},
        'White': {'saturation': 0.0, 'egg_count': 0},
        'Shelby': {'saturation': 0.0, 'egg_count': 0},
        'Ford': {'saturation': 0.0, 'egg_count': 0},
        'Mercer': {'saturation': 0.0, 'egg_count': 0},
        'Iroquois': {'saturation': 0.0, 'egg_count': 0},
        'Washington': {'saturation': 0.0, 'egg_count': 0},
        'Mason': {'saturation': 0.0, 'egg_count': 0},
        'Greene': {'saturation': 0.0, 'egg_count': 0},
        'Hardin': {'saturation': 0.0, 'egg_count': 0},
        'Wayne': {'saturation': 0.0, 'egg_count': 0},
        'Hancock': {'saturation': 0.0, 'egg_count': 0},
        'Brown': {'saturation': 0.0, 'egg_count': 0},
        'Scott': {'saturation': 0.0, 'egg_count': 0},
        'Stark': {'saturation': 0.0, 'egg_count': 0},
        'Jasper': {'saturation': 0.0, 'egg_count': 0},
        'Hamilton': {'saturation': 0.0, 'egg_count': 0},
        'Pike': {'saturation': 0.0, 'egg_count': 0},
        'Henderson': {'saturation': 0.0, 'egg_count': 0},
        'Calhoun': {'saturation': 0.0, 'egg_count': 0},
        'Schuyler': {'saturation': 0.0, 'egg_count': 0},
        'Gallatin': {'saturation': 0.0, 'egg_count': 0},
        'Pope': {'saturation': 0.3, 'egg_count': 300}
    }
    for coef_county in coef_dict:
        for attribute in coef_dict[coef_county]:
            setattr(schema[coef_county], attribute, coef_dict[coef_county][attribute])
    return schema


def iterate_through_years(CG: nx.Graph, schema: dict, neighbor_schema: dict, iterations: int,
                           run_mode='Baseline', use_methods=False) -> pd.DataFrame:
    """
    Takes the initial schema and iterates it through a number of years
    :param use_methods: determines if class methods are used
    :param CG: graph of Illinois network
    :param schema: handler dictionary for graph with name of nodes for keys and County object for values
    :param neighbor_schema: handler dictionary with name of nodes for keys and a list of neighboring County objects
    :param iterations: number of years
    :param run_mode: whether it is baseline mode or another format
    :return cumulative_df: a df that contains the full data for all counties in a run simulation
    """
    # years = input('How many years are you running? \n')
    cumulative_df = make_starting_df(schema)
    year_tracker = 1
    # months_queue = MonthQueue()
    #
    for _ in range(iterations):
        # current_year, traffic_level = years_queue.rotate()
        # if use_methods:
        #     for name, county in schema.items():
        #         county.traffic_level = traffic_level
        #         if current_year in ['May', 'June']:
        #             county.hatch_eggs()
        #         elif current_year in ["August", "September", "October", "November", "December"]:
        #             county.mate()
        #             if current_year in ["September", "October", "November"]:
        #                 county.lay_eggs()
        #         elif current_year in ['January', 'February']:
        #                 county.die_off()
        neighbor_obj = find_neighbor_status(CG, schema)
        schema, cumulative_df = calculate_changes(CG, neighbor_obj, schema, cumulative_df, year_tracker,
                                                  run_mode, use_methods=use_methods)
        year_tracker += 1

    return cumulative_df


def make_starting_df(schema: dict) -> pd.DataFrame:
    """
    Creates an initial dataframe with the list of counties and the starting infection rate for each county
    :param schema:
    :return: instantiated dataframe based on graph handler
    """
    county_list = list(schema[county].name for county in schema)
    starting_saturation = list(schema[county].saturation for county in schema)
    cumulative_df = pd.DataFrame({'County': county_list})
    cumulative_df.insert(1, f'year 0', starting_saturation, True)
    return cumulative_df


def get_object(name: str, schema: dict) -> None:
    """
    Utility function.
    Retrieves the county instance object from the schema when given its name
    :param name: name of object
    :param schema: handler to be searched
    :return:
    """
    for county in schema:
        if county == name:
            return schema[county]



def find_neighbor_status(CG, schema: dict) -> dict:
    """
    Ascertains the saturation status of all neighbors for each county instance,
    returns them as a neighbor object
    :param schema: dictionary handler of graph, with keys as the names of counties and the counties themselves as values
    :param neighbor_schema: dictionary with county names for keys and a list of neighboring county objects.
    :return: the
    """
    neighbor_obj = {}
    for county in schema:
        all_neighbors = []
        for neighbor in schema[county].get_neighbor_objects(CG):
            neighbor = get_object(neighbor.name, schema)
            all_neighbors.append(neighbor)
        neighbor_obj[county] = all_neighbors
    return neighbor_obj


def calculate_changes(CG, neighbor_obj, schema, cumulative_df, year_tracker, run_mode='Baseline', use_methods=False):
    """
    TODO: had a hard time describing this one - Matt
    This iterates outcomes of year interactions

    :param CG: graph of county network
    :param neighbor_obj: the adjacent object
    :param schema: county handler
    :param cumulative_df:
    :param year_tracker: count of current year
    :param run_mode: type of simulation
    :return:
    """
    # print('------------------------- Begin New year -------------------------')
    # if use_methods:
    #     schema, cumulative_df = calc_infest(CG, neighbor_obj, schema, cumulative_df, year_tracker, run_mode=run_mode)
    #     return schema, cumulative_df
    # else:

    saturation_collector = []
    quarantine_list = set()
    for county_net in neighbor_obj:
        all_new_saturations = 0
        county = get_object(county_net, schema)
        county.saturation = county.saturation + (random.normal(0.025, 0.05) *
                                                 (county.saturation * (county.toh_density)))

        for net_neighbors in neighbor_obj[county_net]:
            probability = random.normal(0.5, 0.8)  # random.normal(loc= , scale= )  # SAMPLE EQUATION
            ToH_modifier = (net_neighbors.saturation
                            * (net_neighbors.toh_density)
                            * random.exponential(0.02))
            if run_mode == 'Baseline':
                new_saturation = baseline_calc(net_neighbors, probability, ToH_modifier)
            elif run_mode == 'Poison ToH':
                new_saturation = ToH_calc(net_neighbors, probability, ToH_modifier)
            elif run_mode == 'Population-Based Countermeasures':
                new_saturation = population_calc(county, net_neighbors, probability, ToH_modifier)
            elif run_mode == 'Quarantine':
                quarantine_list, new_saturation = quarantine_calc(quarantine_list, net_neighbors, probability, ToH_modifier)
            elif run_mode == 'All':
                quarantine_list, new_saturation = all_modes(quarantine_list, county, net_neighbors, probability, ToH_modifier)
            else:
                raise ValueError('This is not a valid run mode.')

            all_new_saturations += new_saturation
        all_new_saturations = round(all_new_saturations / (len(neighbor_obj[county_net])), 8) + county.saturation
        all_new_saturations = max(0, min(all_new_saturations, 1))
        # print(f'{county_net} went from {county.saturation} to {all_new_saturations}')
        setattr(county, 'saturation', all_new_saturations)
        saturation_collector.append(all_new_saturations)
    cumulative_df.insert(year_tracker + 1, f'year {year_tracker}', saturation_collector, True)
    return schema, cumulative_df




# def calculate_spread_prob(CG, county, neighbor):
#     """
#     returns the likelyhood of an saturation spreading from one county to another.
#     the spread is based on:
#         - The current saturation level of source county
#         - The combined density of tree of heaven and regular trees
#         - The weight of edge connecting the two counties
#         - The current traffic level of the year
#
#     :param CG: graph of county network
#     :param county: the source node the saturation is spreading from
#     :param neighbor: target node saturation might spread to.
#     :return spread_prob: probability of spread, between 0.0 and 1.0
#     """
#     edge_weight = CG[county][neighbor]['weight']
#     base_prob = random.normal(0.5, 0.2) * county.saturation / (neighbor.toh_density + neighbor.tree_density)
#     spread_prob = base_prob / edge_weight * county.traffic_level
#
#     spread_prob = max(0, min(spread_prob, 1))
#     return spread_prob
#
#
# def spread_saturation(county, neighbor, spread_prob):
#     """
#     updates the saturation level of a neighboring county to source county
#     :param county: source node that saturation spreads from
#     :param neighbor: target node the saturation will spread to
#     :param spread_prob: probability that the saturation will spread
#
#     """
#     max_transferable = county.saturation * spread_prob
#     variablity = random.uniform(0.05, 0.10)
#
#     transfer_amount = max_transferable * variablity
#
#     neighbor.saturation += transfer_amount
#     neighbor.saturation = min(neighbor.saturation, 1.0)
#
#
# def implement_counter_measures(CG, county, neighbor, run_mode):
#     """
#     manipulates saturation and egg levels based on run mode
#     :param CG: graph of county network
#     :param county: county node being assessed
#     :param neighbor: node adjacent to county node
#     :param run_mode: Type of simulation to run
#     """
#     if run_mode == 'Poison ToH':
#         county.die_off(mortality_rate=county.toh_density/1.25)
#         # county.toh_density = county.toh_density - .1 if county.toh_density > 0.0 else county.toh_density
#     elif run_mode in ('Population-Based', 'Quarantine'):
#         county.public_awareness = True if county.saturation >= .5 else county.public_awareness
#         if county.public_awareness:
#             neighbor.public_awareness = True if neighbor.saturation >= county.saturation / 1.5\
#                 else neighbor.public_awareness
#             county.die_off(mortality_rate=county.popdense_sqmi/100000)
#             county.egg_count = county.egg_count - int(county.popdense_sqmi / 1000)
#     elif run_mode == 'All':
#         implement_counter_measures(CG, county, neighbor, run_mode='Poison ToH')
#         implement_counter_measures(CG, county, neighbor, run_mode='Quarantine')
#
#     if run_mode == 'Quarantine':
#         county.quarantine = True if county.saturation >= .75 else county.quarantine
#         if county.quarantine is True:
#             neighbor.public_awareness = True
#             CG[county][neighbor]['weight'] = 2.0
#
#
#
# def calc_infest(CG, neighbor_obj, schema, cumulative_df, year_tracker, run_mode='Baseline'):
#     """
#     updates the new saturation levels for all nodes in county graph.
#     :param CG: The graph of counties
#     :param neighbor_obj: a collection of the neighbors of all nodes.
#     :param schema:
#     :param cumulative_df:
#     :param year_tracker:
#     :param run_mode:
#     :return:
#     """
#     saturation_collector = []
#     infest_data = {}
#
#     for county_net in neighbor_obj:
#         county = get_object(county_net, schema)
#         county.public_awareness = True if county.saturation > .6 else county.public_awareness
#         county.toh_density = county.toh_density + .01  # shows slow growth of ToH, might delete
#         new_saturations = 0
#
#         for net_neighbor in neighbor_obj[county_net]:
#             spread_prob = calculate_spread_prob(CG, county, net_neighbor)
#             implement_counter_measures(CG, county, net_neighbor, run_mode=run_mode)
#             spread_saturation(county, net_neighbor, spread_prob)
#
#             new_saturations += net_neighbor.saturation
#         saturation_collector.append(county.saturation)
#         infest_data[f'year {year_tracker}'] = saturation_collector
#
#     new_trackers = pd.DataFrame(infest_data)
#     cumulative_df = pd.concat([cumulative_df, new_trackers], axis=1)
#     return schema, cumulative_df


def baseline_calc(net_neighbors, probability, ToH_modifier):
    new_saturation = ((net_neighbors.saturation * probability) * 3  + (ToH_modifier * net_neighbors.saturation))/2
    return new_saturation


def ToH_calc(net_neighbors, probability, ToH_modifier):
    ToH_modifier = -ToH_modifier * 100
    new_saturation = net_neighbors.saturation * probability + ToH_modifier * net_neighbors.saturation
    return new_saturation


def population_calc(county, net_neighbors, probability, ToH_modifier):
    bug_smash = random.normal(0.2, 0.1) * 0.01
    new_saturation = (net_neighbors.saturation * probability + ToH_modifier * net_neighbors.saturation - (county.saturation * net_neighbors.popdense_sqmi * bug_smash))
    return new_saturation


def quarantine_calc(quarantine_list, net_neighbors, probability, ToH_modifier):
    if (net_neighbors in quarantine_list) or (net_neighbors.saturation > 0.5 and random.choice([True, False])):
        new_saturation = 0
        quarantine_list.add(net_neighbors)
    else:
        new_saturation = net_neighbors.saturation * probability + ToH_modifier * net_neighbors.saturation
    return quarantine_list, new_saturation


def all_modes(quarantine_list, county, net_neighbors, probability, ToH_modifier):
    if (net_neighbors in quarantine_list) or (net_neighbors.saturation > 0.5 and random.choice([True, False])):
        new_saturation = 0
        quarantine_list.add(net_neighbors)
    else:
        bug_smash = random.normal(0.2, 0.1) * 0.01
        ToH_modifier = -ToH_modifier * 100
        new_saturation = (net_neighbors.saturation * probability +
                           ToH_modifier * net_neighbors.saturation -
                           (county.saturation * net_neighbors.popdense_sqmi * bug_smash))
    return quarantine_list, new_saturation


if __name__ == '__main__':
    df = saturation_main('Population-Based Countermeasures', 10, use_methods=False)
    print(df)