# run_simulation.py

"""
### Authors:
##### Justin Tung:      'https://github.com/JayTongue'
##### Matt Adam-Houser: 'https://github.com/mhouser42'

Takes the output of the illinois network as well as the classes defined as the nodes
inputs parameters for run mode and how long to run the simulation for.
Uses an accumulated dataframe that inserts rows based on each successive year the simulation is run
returns result in a dataframe

TODO: remove unused code
"""

import pickle

import networkx as nx
from numpy import random
import pandas as pd
import json
from my_classes import MonthQueue, County


def saturation_main(run_mode: str, iterations: int, life_cycle=False) -> pd.DataFrame:
    """
    Main Function that sequences the order of events when running this file
    :param run_mode: version of Monte Carlo to run
    :param iterations: number of times to run Monte Carlo
    :param use_methods: a Boolean that decided if saturation is affected by class methods.
    :return cumulative_df: pandas dataframe of cumulative years

    >>> saturation_main('Baseline', -5)
    Traceback (most recent call last):
    ...
    ValueError: Please use an integer greater than zero.
    >>> saturation_main('Poison ToH', 'Hi mom')
    Traceback (most recent call last):
    ...
    ValueError: Please use an integer greater than zero.
    >>> saturation_main('Population-Based Countermeasures', 1.1)
    Traceback (most recent call last):
    ...
    ValueError: Please use an integer greater than zero.
    >>> saturation_main('Parasitic Wasps', 15)  # THIS TEST IS CURRENTLY BLOWING UP DUE TO current_month
    Traceback (most recent call last):
    ...
    ValueError: This is not a valid run mode.
    """
    if type(iterations) == int and iterations > 0:
        CG, schema, neighbor_schema = set_up()
        schema = set_coefficients(schema)
        cumulative_df = iterate_through_timeframe(CG, schema, neighbor_schema, iterations,
                                              run_mode, life_cycle=life_cycle)
            # "Never set a default value on a function parameter that is a literal mutable object."
        return cumulative_df
    else:
        raise ValueError('Please use an integer greater than zero.')


def set_up() -> (nx.Graph, dict, dict):
    """
    return input files created by the illinois_network.py
    :return CG: Picked graph from illinois_network.py
    :return schema: a dict containing each county and its own class instance
    :return neighbor_schema: a dict containing each county and references the instances of adjacent counties

    >>> test_CG = nx.Graph()
    >>> test_schema = {'Cook': object(), 'Pope': object()}
    >>> test_neighbor_schema = {'Cook': [object()], 'Pope': [object()]}
    >>> with open('data/location/IL_graph_test.dat', 'wb') as f:
    ...     pickle.dump(test_CG, f)
    >>> with open('data/location/graph_handler_counties_test.dat', 'wb') as f:
    ...     pickle.dump(test_schema, f)
    >>> with open('data/location/graph_handler_neighbors_test.dat', 'wb') as f:
    ...     pickle.dump(test_neighbor_schema, f)
    >>> result = set_up()
    >>> isinstance(result[0], nx.Graph)
    True
    >>> isinstance(result[1], dict)
    True
    >>> isinstance(result[2], dict)
    True
    """
    prefix = ''
    path = 'data/location'
    CG = pickle.load(open(f'{path}/{prefix}IL_graph.dat', 'rb'))
    schema = pickle.load(open(f'{path}/{prefix}graph_handler_counties.dat', 'rb'))
    neighbor_schema = pickle.load(open(f'{path}/{prefix}graph_handler_neighbors.dat', 'rb'))
    return CG, schema, neighbor_schema


def set_coefficients(schema: dict) -> dict:
    """
      Sets coefficients for the class attributes
      Changes the attributes within the schema
      :param schema: handler for dictionary
      :return: handler but updated

      >>> class County:
      ...     def __init__(self, name, infestation, pop, toh):
      ...         self.name = name
      ...         self.infestation = infestation
      ...         self.pop = pop
      ...         self.toh = toh
      >>> Pope = County('Pope', 0, 0, 0)
      >>> Cook = County('Cook', 0, 0, 0)
      >>> schema_test = {'Pope': Pope, 'Cook': Cook}
      >>> updated_schema = set_coefficients(schema_test)
      >>> isinstance(updated_schema, dict)
      True
      >>> all(hasattr(county, 'infestation') for county in updated_schema.values())
      True
      >>> any(hasattr(county, 'toh') for county in updated_schema.values())
      True
      """
    coef_dict = open('data/coef_dict.JSON')
    coef_dict = json.load(coef_dict)
    for coef_county in coef_dict:
        for attribute in coef_dict[coef_county]:
            try:  # Attempts to load coefficients and set starting corresponding attributes from the coefficient JSON.
                setattr(schema[coef_county], attribute, coef_dict[coef_county][attribute])
            except KeyError:
                continue
    return schema


def iterate_through_timeframe(CG: nx.Graph, schema: dict, neighbor_schema: dict, iterations: int,
                              run_mode='Baseline', life_cycle=False) -> pd.DataFrame:
    """
    Takes the initial schema and iterates it through a number of years
    :param CG: graph of Illinois network
    :param schema: handler dictionary for graph with name of nodes for keys and County object for values
    :param neighbor_schema: handler dictionary with name of nodes for keys and a list of neighboring County objects
    :param iterations: number of years
    :param run_mode: whether it is baseline mode or another format
    :param use_methods: determines if class methods are used
    :return cumulative_df: a df that contains the full data for all counties in a run simulation

    # I cannot for the life of me figure out how to get this to work
    # >>> class County:
    # ...     def __init__(self, name, saturation, toh_density):
    # ...         self.name = name
    # ...         self.saturation = saturation
    # ...         self.toh_density = toh_density
    # ...     def get_neighbor_objects(self, name):
    # ...         return []
    #
    # >>> schema = {}
    # >>> CG = nx.Graph()
    # >>> for county in ['Coles', 'Bond', 'Edwards', 'Kane', 'Macon']:
    # ...     county_obj = County(county, 0.5, 0.3)
    # ...     schema[county] = county_obj
    # >>> neighbor_schema = {'Coles': ['Edwards', 'Kane', 'Macon'], 'Bond': ['Edwards', 'Kane', 'Macon']}
    # >>> test_iterations = 5
    # >>> test_df = iterate_through_years(CG, schema, neighbor_schema, test_iterations)
    # >>> isinstance(test_df, pd.DataFrame)
    # True
    # >>> len(test_df)
    # 5

    """
    cumulative_df = make_starting_df(schema, time_frame='month') if life_cycle else make_starting_df(schema)
    year_tracker = 1
    months_queue = MonthQueue()

    for _ in range(iterations):
        neighbor_obj = find_neighbor_status(CG, schema)
        schema, cumulative_df = calculate_changes(CG, neighbor_obj, schema, cumulative_df, year_tracker, current_month,
                                                  run_mode, life_cycle=0)
        year_tracker += 1

        current_month = months_queue.rotate()
        if life_cycle:
            for name, county in schema.items():
                county.traffic_level = current_month['traffic_level']
                if current_month in ['May', 'June']:
                    county.hatch_eggs()
                elif current_month in ['August', 'September', 'October', 'November', 'December']:
                    county.mate()
                    if current_month in ['September', 'October', 'November']:
                        county.lay_eggs()
                elif current_month in ['January', 'February']:
                    county.die_off(1.0)


    return cumulative_df


def make_starting_df(schema: dict, time_frame='year') -> pd.DataFrame:
    """
    Creates an initial dataframe with the list of counties and the starting infection rate for each county
    :param schema:
    :return: instantiated dataframe based on graph handler

    >>> class County:
    ...     def __init__(self, name, saturation):
    ...         self.name = name
    ...         self.saturation = saturation
    >>> counties = {'Mercer': County('Mercer', 0.2), 'Perry': County('Perry', 0.5)}
    >>> df = make_starting_df(counties)
    >>> isinstance(df, pd.DataFrame)
    True
    >>> df.columns.tolist()
    ['County', 'year 0']
    >>> len(df)
    2
    >>> df.loc[df['County'] == 'Mercer', 'year 0'].values[0]
    0.2
    >>> df.loc[df['County'] == 'Perry', 'year 0'].values[0]
    0.5
    """
    county_list = list(schema[county].name for county in schema)
    starting_saturation = list(schema[county].saturation for county in schema)
    cumulative_df = pd.DataFrame({'County': county_list})
    cumulative_df.insert(1, f'{time_frame} 0', starting_saturation, True)
    return cumulative_df


def get_object(name: str, schema: dict) -> County:
    """
    Utility function.
    Retrieves the county instance object from the schema when given its name
    :param name: name of object
    :param schema: handler to be searched
    :return schmea[county]: the object that corresponds to the name in the schema

    >>> class County:
    ...     def __init__(self, name):
    ...         self.name = name
    >>> counties = {'Richland': County('Richland'), 'Scott': County('Scott')}
    >>> obj_a = get_object('Richland', counties)
    >>> isinstance(obj_a, County)  # Check if object returned is an instance of County
    True
    >>> obj_a.name  # Check the name of the retrieved object
    'Richland'
    >>> obj_b = get_object('Scott', counties)
    >>> isinstance(obj_b, County)  # Check if object returned is an instance of County
    True
    >>> obj_b.name  # Check the name of the retrieved object
    'Scott'
    >>> get_object('Travis', counties) is None  # Check if non-existent object returns None
    True
    """
    for county in schema:
        if county == name:
            return schema[county]


def find_neighbor_status(CG: nx.Graph, schema: dict) -> dict:
    """
    Ascertains the saturation status of all neighbors for each county instance,
    returns them as a neighbor object
    :param CG: the network graph of counties
    :param schema: dictionary handler of graph, with keys as the names of counties and the counties themselves as values
    :return neighbor_obj: the dict county objects

    >>> class County:
    ...     def __init__(self, name):
    ...         self.name = name
    ...     def get_neighbor_objects(self, CG):
    ...         return [County('Stark'), County('Neighbor B')]
    >>> counties = {'Stark': County('Stark'), 'Massac': County('Massac')}
    >>> CG = {}  # Your graph here
    >>> neighbors = find_neighbor_status(CG, counties)
    >>> isinstance(neighbors, dict)  # Check if the returned value is a dictionary
    True
    >>> len(neighbors)  # Check if the dictionary has expected length based on the number of counties
    2
    >>> isinstance(neighbors['Stark'], list)  # Check if the neighbors are returned as lists
    True
    >>> len(neighbors['Stark'])
    2
    >>> neighbors['Stark'][0].name
    'Stark'
    >>> neighbors['Stark'][10].name
    Traceback (most recent call last):
    ...
    IndexError: list index out of range
    >>> len(neighbors['Massac'])  # Check the number of neighbors for County B
    2
    """
    neighbor_obj = {}
    for county in schema:
        all_neighbors = []
        for neighbor in schema[county].get_neighbor_objects(CG):
            neighbor = get_object(neighbor.name, schema)
            all_neighbors.append(neighbor)
        neighbor_obj[county] = all_neighbors
    return neighbor_obj


def calculate_changes(CG: nx.Graph, neighbor_obj: dict, schema: dict, cumulative_df: pd.DataFrame,
                      year_tracker: int, run_mode='Baseline', use_methods=False):
    """
    Models interactions between every county and every county it is adjacent to
    This is a yearly interaction
    calculates one county's change in saturation based on the counties adjoining it

    :param CG: graph of county network
    :param neighbor_obj: the adjacent object
    :param schema: county handler
    :param cumulative_df: a dataframe that stores saturation levels from year to year for each county
    :param year_tracker: count of current year
    :param run_mode: type of simulation
    :return schema: a dict of counties and their objects
    :return cumulative_df: the df used to record, store, and access saturation rates

    # going to have trouble doctesting this because it's not deterministic
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
        all_new_saturations = process_net_neighbors(all_new_saturations, county, county_net, neighbor_obj,
                                                    quarantine_list, run_mode)
        all_new_saturations = round(all_new_saturations / (len(neighbor_obj[county_net])), 8) + county.saturation
        all_new_saturations = max(0, min(all_new_saturations, 1)) # keeps all_new_saturations between 0 and 1
        setattr(county, 'saturation', all_new_saturations) # changes the county instance attribute
        saturation_collector.append(all_new_saturations)  # Adds the saturation to a list
    cumulative_df.insert(year_tracker + 1, f'year {year_tracker}', saturation_collector, True) # adds list to df
    return schema, cumulative_df


def process_net_neighbors(all_new_saturations: float, county: County, county_net: County,
                          neighbor_obj: dict, quarantine_list: set, run_mode: str) -> float:
    """
    calculates neighbor county influence on the target county and
    generates random statistics for ToH and base probability
    Assigns calculations to the correct run mode function
    :param all_new_saturations: an accumulator of all neighbor saturations beginning with 0
    :param county: the target county target
    :param county_net: an iterated network for the neighbor_obj, the target county's network objs
    :param neighbor_obj: the total list of neighbor objects
    :param quarantine_list: the set of quarantining counties
    :param run_mode: a string defining run_mode
    :return all_new_saturations: float of the accumulated all new saturations

    >>> class County:
    ...     def __init__(self, name, saturation, toh_density):
    ...         self.name = name
    ...         self.saturation = saturation
    ...         self.toh_density = toh_density
    >>> Clark = County('Clark', 0.5, 0.6)
    >>> Mennard = County('Mennard', 0.7, 0.8)
    >>> LaSalle = County('LaSalle', 0.3, 0.4)
    >>> neighbor_obj = {Clark: [Mennard, LaSalle], Mennard: [Clark, LaSalle], LaSalle: [Clark, Mennard]}
    >>> quarantine_set = set()
    >>> run_mode = 'Baseline'
    >>> def assign_mode(ToH_modifier, county, net_neighbors, probability, quarantine_list, run_mode):
    ...     return ToH_modifier * net_neighbors.saturation * probability
    >>> result = process_net_neighbors(0, Clark, Clark, neighbor_obj, quarantine_set, run_mode)
    >>> isinstance(result, float)
    True

    """
    for net_neighbors in neighbor_obj[county_net]:
        probability = random.normal(0.45, 0.8)
        ToH_modifier = (net_neighbors.saturation
                        * (net_neighbors.toh_density) * 100
                        * random.exponential(0.02))
        new_saturation = assign_mode(ToH_modifier, county, net_neighbors, probability, quarantine_list, run_mode)
        all_new_saturations += new_saturation
    return all_new_saturations


def assign_mode(ToH_modifier: float, county: County, net_neighbors: County, probability: float,
                quarantine_list: set, run_mode: str) -> float:
    """
    a hub that sends variables to the correct processing function depending on the selected run_mode
    catches invalid run modes
    :param ToH_modifier: a modifier that represents the effect ToH have on SLF populations
    :param county: the target county object
    :param net_neighbors: the neighboring county objects
    :param probability: the probability of transmission from one county to another
    :param quarantine_list: the set of counties that have decided to quarantine
    :param run_mode: the run mode selected as an input variable
    :return new_saturation: the new saturation of the target county object.

    >>> class County:
    ...     def __init__(self, name, saturation):
    ...         self.name = name
    ...         self.saturation = saturation
    >>> Williamson = County('Williamson', 0.5)
    >>> Ogle = County('Ogle', 0.7)
    >>> Lee = County('Lee', 0.3)
    >>> quarantine_set = {Williamson}
    >>> def baseline_calc(net_neighbors, probability, ToH_modifier):
    ...     return net_neighbors.saturation * probability + ToH_modifier * net_neighbors.saturation
    >>> def ToH_calc(net_neighbors, probability, ToH_modifier):
    ...     return net_neighbors.saturation * probability + ToH_modifier * net_neighbors.saturation
    >>> def population_calc(county, net_neighbors, probability, ToH_modifier):
    ...     return net_neighbors.saturation * probability + ToH_modifier * net_neighbors.saturation - county.saturation
    >>> def quarantine_calc(quarantine_list, net_neighbors, probability, ToH_modifier):
    ...     return quarantine_list, net_neighbors.saturation * probability + ToH_modifier * net_neighbors.saturation
    >>> def all_modes(quarantine_list, county, net_neighbors, probability, ToH_modifier):
    ...     return quarantine_list, net_neighbors.saturation * probability + ToH_modifier * net_neighbors.saturation
    >>> result_baseline = assign_mode(0.5, Williamson, Ogle, 0.8, set(), 'Baseline')
    >>> isinstance(result_baseline, float)  # Check if the result is a float
    True

    """
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
    else:  # catches invalid run modes
        raise ValueError('This is not a valid run mode.')
    return new_saturation

def baseline_calc(net_neighbors: County, probability: float, ToH_modifier: float) -> float:
    """
    A baseline calculation that serves as a an initial model to modify for different interventions
    :param net_neighbors: the particualr instance of an neighbor object used to change saturation
    :param probability: the random probability of infection on a normal distribution
    :param ToH_modifier: the maount that ToH chances the succeptability to SLF
    :return new_saturation: the new amount of saturation for that county

    >>> class County:
    ...     def __init__(self, saturation):
    ...         self.saturation = saturation
    >>> neighbor = County(0.5)
    >>> probability_value = 0.7
    >>> ToH_value = 0.
    >>> new_saturation = baseline_calc(neighbor, probability_value, ToH_value)
    >>> isinstance(new_saturation, float)
    True
    >>> new_saturation
    0.5249999999999999
    """
    new_saturation = ((net_neighbors.saturation * probability) * 3 + (ToH_modifier * net_neighbors.saturation)) / 2
    return new_saturation


def ToH_calc(net_neighbors: County, probability: float, ToH_modifier: float) -> float:
    """
    A variation on baseline that modifies the effect of ToH to represent an intervention
    :param net_neighbors: the neighboring object
    :param probability: a random probability on a normal distribution
    :param ToH_modifier: a randomized representation of the ToH modification
    :return new_saturation: the new infection from the target county to the neighbor.

    >>> class County:
    ...     def __init__(self, saturation):
    ...         self.saturation = saturation
    >>> neighbor = County(0.5)
    >>> probability_value = 0.7
    >>> ToH_value = 0.002
    >>> ToH_calc(neighbor, probability_value, ToH_value)
    0.349
    >>> isinstance(ToH_calc(neighbor, probability_value, ToH_value), float)
    True
    """
    ToH_modifier = -ToH_modifier
    new_saturation = net_neighbors.saturation * probability + ToH_modifier * net_neighbors.saturation
    return new_saturation


def population_calc(county: County, net_neighbors: County, probability: float, ToH_modifier: float) -> float:
    """
    A modification of the baseline that models what may happen if citizen of a county
    were inclined and educated to help eliminate SLF and their eggs
    :param county: the object of the target county
    :param net_neighbors: the object of the neighboring county
    :param probability: random probability of transmission based on a normal distribution
    :param ToH_modifier: random probability that transmission will influenced by ToH
    :return new_infection: the new infection level from neighbor to target county

    >>> class County:
    ...     def __init__(self, saturation, popdense_sqmi):
    ...         self.saturation = saturation
    ...         self.popdense_sqmi = popdense_sqmi
    >>> neighbor = County(0.5, 500)
    >>> target = County(0.3, 300)
    >>> probability_value = 5  # this is outrageously high to make sure the test is reliable
    >>> ToH_value = 0.1
    >>> new_infection = population_calc(target, neighbor, probability_value, ToH_value)
    >>> isinstance(new_infection, float)
    True
    >>> new_infection > 0
    True
    """
    bug_smash = random.normal(0.2, 0.1) * 0.01
    new_saturation = (net_neighbors.saturation * probability + ToH_modifier * net_neighbors.saturation
                      - (county.saturation * net_neighbors.popdense_sqmi * bug_smash))
    return new_saturation


def quarantine_calc(quarantine_list: set, net_neighbors: County,
                    probability: float, ToH_modifier: float) -> (set, float):
    """
    Modification of baseline that models what would happen if
    a county, reaching 50% of saturation, had a 50% chance of quarantining with 100% efficacy
    counties are stored persistently if they decide to quarantine.
    :param quarantine_list: not a list, but actually a set of the counties that are quarantined
    :param net_neighbors: neighbor object
    :param probability: probability on a normal distribution of transmission from one county to another
    :param ToH_modifier: probability of ToH influencing saturation
    :return quarantine_list: the new set of quarantining counties, possibly with the target added.
    :return new_infection: the new infection rate from a neighbor to a target county

    >>> class County:
    ...     def __init__(self, saturation, popdense_sqmi):
    ...         self.saturation = saturation
    ...         self.popdense_sqmi = popdense_sqmi
    >>> neighbor = County(0.5, 500)
    >>> target = County(0.3, 300)
    >>> probability_value = 0.002
    >>> ToH_value = 0.1
    >>> new_infection = population_calc(target, neighbor, probability_value, ToH_value)
    >>> isinstance(new_infection, float)
    True
    """
    if (net_neighbors in quarantine_list) or (net_neighbors.saturation > 0.5 and random.choice([True, False])):
        new_saturation = 0
        quarantine_list.add(net_neighbors)
    else:
        new_saturation = net_neighbors.saturation * probability + ToH_modifier * net_neighbors.saturation
    return quarantine_list, new_saturation


def all_modes(quarantine_list: set, county: County, net_neighbors: County, probability: float,
              ToH_modifier: float) -> (set, float):
    """
    A variation of baseline that includes all interventions modeled in all other functions

    :param quarantine_list: not a list, but a set of quarantining counties
    :param county: target county object
    :param net_neighbors: neighboring county object
    :param probability: the probabiltiy, on a normal distribution, that one county infects a neighbor
    :param ToH_modifier: the probabilty that extant ToH populations will influence saturation growth
    :return quarantine_list: the new set of quarantining counties, possibly with the target added.
    :return new_infection: the new infection rate from a neighbor to a target county

    >>> class County:
    ...     def __init__(self, saturation, popdense_sqmi):
    ...         self.saturation = saturation
    ...         self.popdense_sqmi = popdense_sqmi
    >>> quarantine_set = set()
    >>> target_county = County(0.2, 100)
    >>> Cook = County(0.3, 150)
    >>> Pope = County(0.7, 80)
    >>> quarantine_list, new_saturation_1 = all_modes(quarantine_set, target_county, Cook, 0.5, 0.1)
    >>> isinstance(quarantine_list, set)
    True
    >>> isinstance(new_saturation_1, float)
    True
    >>> quarantine_list, new_saturation_2 = all_modes(quarantine_list, target_county, Pope, 0.5, 0.1)
    >>> isinstance(quarantine_list, set)
    True
    """

    if (net_neighbors in quarantine_list) or (net_neighbors.saturation > 0.5 and random.choice([True, False])):
        new_saturation = 0
        quarantine_list.add(net_neighbors)
    else:
        bug_smash = random.normal(0.2, 0.1) * 0.01
        ToH_modifier = -ToH_modifier
        new_saturation = (net_neighbors.saturation * probability +
                          ToH_modifier * net_neighbors.saturation -
                          (county.saturation * net_neighbors.popdense_sqmi * bug_smash))
    return quarantine_list, new_saturation

def calculate_spread_prob(CG, county, neighbor):
    """
    returns the likelyhood of an saturation spreading from one county to another.
    the spread is based on:
        - The current saturation level of source county
        - The combined density of tree of heaven and regular trees
        - The weight of edge connecting the two counties
        - The current traffic level of the month

    :param CG: graph of county network
    :param county: the source node the saturation is spreading from
    :param neighbor: target node saturation might spread to.
    :return spread_prob: probability of spread, between 0.0 and 1.0
    """
    edge_weight = CG[county][neighbor]['weight']
    base_prob = random.normal(0.3, 0.2) * county.saturation / (neighbor.toh_density + neighbor.tree_density)
    spread_prob = base_prob / edge_weight * county.traffic_level

    spread_prob = max(0, min(spread_prob, 1))
    return spread_prob


def spread_saturation(county, neighbor, spread_prob, current_month=0):
    """
    updates the saturation level of a neighboring county to source county
    :param county: source node that saturation spreads from
    :param neighbor: target node the saturation will spread to
    :param spread_prob: probability that the saturation will spread

    """
    max_transferable = county.saturation * spread_prob
    variablity = random.uniform(0.05, 0.10)

    transfer_amount = max_transferable * variablity

    neighbor.saturation += transfer_amount
    neighbor.saturation = min(neighbor.saturation, 1.0)
    if current_month in ['September', 'October', 'November']:
        neighbor.egg_count += int(transfer_amount * 100)


def implement_counter_measures(CG, county, neighbor, run_mode):
    """
    Manipulates saturation and egg levels based on run mode
    :param CG: graph of county network
    :param county: county node being assessed
    :param neighbor: node adjacent to county node
    :param run_mode: Type of simulation to run
    """
    if run_mode == 'Poison ToH':
        county.die_off(mortality_rate=county.toh_density/65)
        # county.toh_density = county.toh_density - .01 if county.toh_density > 0.0 else county.toh_density
    elif run_mode in ('Population-Based', 'Quarantine'):
        implement_pop_kill(county, neighbor)
    elif run_mode == 'All':
        implement_counter_measures(CG, county, neighbor, run_mode='Poison ToH')
        implement_counter_measures(CG, county, neighbor, run_mode='Quarantine')

    if run_mode == 'Quarantine':
        implement_quarantine(CG, county, neighbor)


def implement_pop_kill(county, neighbor):
    """
    Toggles county's public_awareness if they reach certain thresholds.
    If the county is aware, triggers die_off and egg removal based off population density.

    Can also toggle neighbor's public awareness at certain thresholds.
    :param county: County obj being assessed
    :param neighbor: neighboring county
    """
    if neighbor.quarantine:
        county.public_awareness = True if county.saturation >= neighbor.saturation/2 else county.public_awareness
    county.public_awareness = False if county.saturation <= .20 else county.public_awareness
    if county.public_awareness:
        neighbor.public_awareness = True if neighbor.saturation >= county.saturation / 2 \
            else neighbor.public_awareness
        county.die_off(mortality_rate=county.popdense_sqmi / 7500)
        county.egg_count = county.egg_count - int(county.popdense_sqmi / 1000)


def implement_quarantine(CG, county, neighbor):
    """
    Toggles a county's quarantine once it reaches certain thresholds.
    Toggles neighbor's public awareness if its saturation is half of quarantine
    Changes wieght of edge between county and neighbor if certain conditions are met.

    :param CG: Network Graph
    :param county: County node object
    :param neighbor: County node object connected to county by edge.
    """
    county.quarantine = True if county.saturation >= .75 else county.quarantine
    county.quarantine = False if county.saturation <= .25 else county.quarantine
    if county.quarantine is True:
        neighbor.public_awareness = True
        CG[county][neighbor]['weight'] = 2
    elif county.quarantine is False and neighbor.quarantine is True:
        pass
    elif CG[county][neighbor]['rel'] == 'interstate':
        CG[county][neighbor]['weight'] = .25
    else:
        CG[county][neighbor]['weight'] = 1.0


def calc_infest(CG, neighbor_obj, schema, cumulative_df, month_tracker, current_month, run_mode='Baseline'):
    """
    updates the new saturation levels for all nodes in county graph.
    :param CG: The graph of counties
    :param neighbor_obj: a collection of the neighbors of all nodes.
    :param schema:
    :param cumulative_df:
    :param month_tracker:
    :param run_mode:
    :return:
    """
    saturation_collector = []
    infest_data = {}

    for county_net in neighbor_obj:
        county = schema[county_net]
        county.public_awareness = True if county.saturation > .6 else county.public_awareness
        county.toh_density = county.toh_density + .01  # shows slow growth of ToH, might delete
        new_saturations = 0

        for net_neighbor in neighbor_obj[county_net]:
            spread_prob = calculate_spread_prob(CG, county, net_neighbor)
            implement_counter_measures(CG, county, net_neighbor, run_mode=run_mode)
            spread_saturation(county, net_neighbor, spread_prob, current_month=current_month)

            new_saturations += net_neighbor.saturation
        saturation_collector.append(county.saturation)
        infest_data[f'month {month_tracker}'] = saturation_collector

    new_trackers = pd.DataFrame(infest_data)
    cumulative_df = pd.concat([cumulative_df, new_trackers], axis=1)
    return schema, cumulative_df


if __name__ == '__main__':
    saturation_main('Quarantine', 15, life_cycle=True)
