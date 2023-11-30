"""
TODO: Change coef_dict to reflect actual fly saturation levels [MATT]
"""

import pickle
from numpy import random
import pandas as pd


def saturation_main(run_mode, iterations):
    """
    Main Function that sequences the order of events when running this file
    :param run_mode: version of Monte Carlo to run
    :param iterations: number of times to run Monte Carlo
    :return : pandas dataframe of cumulative years
    """
    CG, schema = set_up()
    schema = set_coefficients(schema)
    cumulative_df = year(CG, schema, iterations, run_mode)
    return cumulative_df


def set_up():
    """
    Sets up input files
    :return:
    """
    path = 'data/location'
    CG = pickle.load(open(f'{path}/IL_graph.dat', 'rb'))
    schema = pickle.load(open(f'{path}/graph_handler_counties.dat', 'rb'))
    return CG, schema


def set_coefficients(schema):
    """
    Sets coefficients for the class attribues
    Changes the attributes within the schema
    :param schema: handler for dictionary
    :return:

    TODO: Make the Dict here reflect actual levels of things [MATT]
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


def year(CG, schema, iterations, run_mode):
    """
    Takes the initial schema and iterates it through a number of years
    :param CG: graph of Illinois network
    :param schema: handler dictionary for graph
    :param iterations: number
    :param run_mode:
    :return:
    """
    # years = input('How many years are you running? \n')
    cumulative_df = make_starting_df(schema)
    year_tracker = 1
    for i in range(0, int(iterations)):
        neighbor_obj = find_neighbor_status(CG, schema)
        schema, cumulative_df = calculate_changes(neighbor_obj, schema, cumulative_df, year_tracker, run_mode)
        year_tracker += 1

    return cumulative_df


def make_starting_df(schema):
    county_list = list(schema[county].name for county in schema)
    starting_saturation = list(schema[county].saturation for county in schema)
    cumulative_df = pd.DataFrame({'County': county_list})
    cumulative_df.insert(1, f'year 0', starting_saturation, True)
    return cumulative_df


def find_neighbor_status(CG, schema):
    """
    Ascertains the saturation status of all neighbors for each county instance,
    returns them as a neighbor object
    :param CG:
    :param schema:
    :return:
    """
    neighbor_obj = {}
    for county in schema:
        all_neighbors = []
        for neighbor in schema[county].get_neighbor_objects(CG):
            neighbor = get_object(neighbor.name, schema)
            all_neighbors.append(neighbor)
        neighbor_obj[county] = all_neighbors
    return neighbor_obj


def get_object(name, schema):  # I'm not certain this loop is necessary, you should just be able to do schema[name]
    # and get same result without iterating through loop -Matt
    """
    Utility function.
    Retrieves the county instance object from the schema when given its name
    :param name:
    :param schema:
    :return:
    """
    for county in schema:
        if county == name:
            return schema[county]


def calculate_changes(neighbor_obj, schema, cumulative_df, year_tracker, run_mode):
    """
    SUPER TENTATIVE
    This iterates outcomes of year interactions randomly
    :param neighbor_obj:
    :param schema:
    :return:

    TODO: Figure out how to model the actual math here.
    TODO: Establish run modes
    """

    # print('------------------------- Begin New year -------------------------')
    saturation_collector = []
    quarantine_list = set()
    for county_net in neighbor_obj:
        all_new_saturations = 0
        county = get_object(county_net, schema)
        county.saturation = county.saturation + (random.normal(0.025, 0.05) *
                                                 (county.saturation * (county.toh_density_percentile / 100)))
        for net_neighbors in neighbor_obj[county_net]:
            probability = random.normal(0.5, 0.8)  # random.normal(loc= , scale= )  # SAMPLE EQUATION
            if run_mode == 'Baseline':
                new_saturation = baseline_calc(net_neighbors, probability)
            elif run_mode == 'Poison ToH':
                new_saturation = ToH_calc(net_neighbors, probability)
            elif run_mode == 'Population-Based Countermeasures':
                new_saturation = population_calc(county, net_neighbors, probability)
            elif run_mode == 'Quarantine':
                quarantine_list, new_saturation = quarantine_calc(quarantine_list, net_neighbors, probability)
            elif run_mode == 'All':
                quarantine_list, new_saturation = all_modes(quarantine_list, county, net_neighbors, probability)
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


def baseline_calc(net_neighbors, probability):

    ToH_modifier = (net_neighbors.saturation
                    * (net_neighbors.toh_density_percentile)
                    * random.exponential(0.02))
    new_saturation = ((net_neighbors.saturation * probability) * 3  + (ToH_modifier * net_neighbors.saturation))/2
    return new_saturation


def ToH_calc(net_neighbors, probability):
    ToH_modifier = -(net_neighbors.saturation ** 2
                    * net_neighbors.toh_density_percentile
                    * random.exponential(0.02))
    new_saturation = net_neighbors.saturation * probability + ToH_modifier * net_neighbors.saturation
    return new_saturation


def population_calc(county, net_neighbors, probability):
    bug_smash = random.normal(0.2, 0.1) * 0.01
    ToH_modifier = (net_neighbors.saturation ** 2
                    * net_neighbors.toh_density_percentile
                    * random.exponential(0.02))
    # print((1/net_neighbors.popdense_sqmi) * county.saturation)
    new_saturation = (net_neighbors.saturation * probability +
                       ToH_modifier * net_neighbors.saturation -
                       (county.saturation * net_neighbors.popdense_sqmi * bug_smash))
    return new_saturation


def quarantine_calc(quarantine_list, net_neighbors, probability):
    if (net_neighbors in quarantine_list) or (net_neighbors.saturation > 0.5 and random.choice([True, False])):
        new_saturation = 0
        quarantine_list.add(net_neighbors)
    else:
        ToH_modifier = (net_neighbors.saturation ** 2
                        * net_neighbors.toh_density_percentile
                        * random.exponential(0.02))
        new_saturation = net_neighbors.saturation * probability + ToH_modifier * net_neighbors.saturation
    return quarantine_list, new_saturation


def all_modes(quarantine_list, county, net_neighbors):
    if (net_neighbors in quarantine_list) or (net_neighbors.saturation > 0.5 and random.choice([True, False])):
        new_saturation = 0
        quarantine_list.add(net_neighbors)
    else:
        probability = random.normal(0.5, 0.8)
        bug_smash = random.normal(0.2, 0.1) * 0.01
        ToH_modifier = -(net_neighbors.saturation ** 2
                        * net_neighbors.toh_density_percentile
                        * random.exponential(0.02))
        new_saturation = (net_neighbors.saturation * probability +
                           ToH_modifier * net_neighbors.saturation -
                           (county.saturation * net_neighbors.popdense_sqmi * bug_smash))
    return quarantine_list, new_saturation


if __name__ == '__main__':
    df = saturation_main('All', 10)
    print(df)