"""
TODO: Change coef_dict to reflect actual fly infestation levels [MATT]
"""

import pickle
from numpy import random
import pandas as pd


def infestation_main(run_mode, iterations):
    """
    Main Function that sequences the order of events when running this file
    :param run_mode: version of Monte Carlo to run
    :param iterations: number of times to run Monte Carlo
    :return : pandas dataframe of cumulative months
    """
    CG, schema = set_up()
    schema = set_coefficients(schema)
    cumulative_df = month(CG, schema, iterations, run_mode)
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

    coef_dict = {  # This is where we can adjust parameters. Should we save this in an exported JSON?
        'Cook': {'infestation': 0.1},  # The idea was to set up a dict we could use for all attributes we want
        'DuPage': {'infestation': 0},
        'Kane': {'infestation': 0.3},
        'Will': {'infestation': 0},
        'Winnebago': {'infestation': 0},
        'Lake': {'infestation': 0},
        'McHenry': {'infestation': 0},
        'St. Clair': {'infestation': 0},
        'Kendall': {'infestation': 0},
        'Madison': {'infestation': 0.5},
        'Rock Island': {'infestation': 0},
        'Peoria': {'infestation': 0},
        'Sangamon': {'infestation': 0},
        'Tazewell': {'infestation': 0},
        'Champaign': {'infestation': 0.8},
        'Boone': {'infestation': 0},
        'Macon': {'infestation': 0},
        'Kankakee': {'infestation': 0},
        'DeKalb': {'infestation': 0},
        'Williamson': {'infestation': 0},
        'McLean': {'infestation': 0},
        'Grundy': {'infestation': 0.1},
        'Coles': {'infestation': 0},
        'Jackson': {'infestation': 0},
        'LaSalle': {'infestation': 0},
        'Franklin': {'infestation': 0},
        'Vermilion': {'infestation': 0},
        'Monroe': {'infestation': 0},
        'Stephenson': {'infestation': 0.6},
        'Whiteside': {'infestation': 0},
        'Adams': {'infestation': 0},
        'Clinton': {'infestation': 0},
        'Knox': {'infestation': 0},
        'Woodford': {'infestation': 0},
        'Effingham': {'infestation': 0},
        'Ogle': {'infestation': 0.3},
        'Marion': {'infestation': 0},
        'Jefferson': {'infestation': 0},
        'Saline': {'infestation': 0},
        'Massac': {'infestation': 0},
        'Morgan': {'infestation': 0},
        'Henry': {'infestation': 0},
        'Jersey': {'infestation': 0},
        'Randolph': {'infestation': 0},
        'McDonough': {'infestation': 0},
        'Macoupin': {'infestation': 0},
        'Wabash': {'infestation': 0},
        'Perry': {'infestation': 0},
        'Logan': {'infestation': 0},
        'Lee': {'infestation': 0},
        'Christian': {'infestation': 0},
        'Douglas': {'infestation': 0},
        'Bond': {'infestation': 0},
        'Lawrence': {'infestation': 0},
        'Richland': {'infestation': 0},
        'Crawford': {'infestation': 0},
        'Moultrie': {'infestation': 0},
        'Montgomery': {'infestation': 0},
        'Union': {'infestation': 0},
        'Fulton': {'infestation': 0},
        'DeWitt': {'infestation': 0},
        'Menard': {'infestation': 0},
        'Bureau': {'infestation': 0},
        'Piatt': {'infestation': 0},
        'Livingston': {'infestation': 0},
        'Johnson': {'infestation': 0},
        'Jo Daviess': {'infestation': 0},
        'Cass': {'infestation': 0},
        'Putnam': {'infestation': 0},
        'Warren': {'infestation': 0},
        'Carroll': {'infestation': 0},
        'Clark': {'infestation': 0},
        'Cumberland': {'infestation': 0},
        'Alexander': {'infestation': 0},
        'Marshall': {'infestation': 0},
        'Fayette': {'infestation': 0},
        'Edwards': {'infestation': 0},
        'Pulaski': {'infestation': 0},
        'Clay': {'infestation': 0},
        'Edgar': {'infestation': 0},
        'White': {'infestation': 0},
        'Shelby': {'infestation': 0},
        'Ford': {'infestation': 0},
        'Mercer': {'infestation': 0},
        'Iroquois': {'infestation': 0},
        'Washington': {'infestation': 0},
        'Mason': {'infestation': 0},
        'Greene': {'infestation': 0},
        'Hardin': {'infestation': 0},
        'Wayne': {'infestation': 0},
        'Hancock': {'infestation': 0},
        'Brown': {'infestation': 0},
        'Scott': {'infestation': 0},
        'Stark': {'infestation': 0},
        'Jasper': {'infestation': 0},
        'Hamilton': {'infestation': 0},
        'Pike': {'infestation': 0},
        'Henderson': {'infestation': 0},
        'Calhoun': {'infestation': 0},
        'Schuyler': {'infestation': 0},
        'Gallatin': {'infestation': 0},
        'Pope': {'infestation': 0}
    }
    for coef_county in coef_dict:
        for attribute in coef_dict[coef_county]:
            setattr(schema[coef_county], attribute, coef_dict[coef_county][attribute])
    return schema


def month(CG, schema, iterations, run_mode):
    """
    Takes the initial schema and iterates it through a number of months
    :param CG: graph of Illinois network
    :param schema: handler dictionary for graph
    :param iterations: number
    :param run_mode:
    :return:
    """
    # months = input('How many months are you running? \n')
    cumulative_df = make_starting_df(schema)
    month_tracker = 1
    for i in range(0, int(iterations)):
        neighbor_obj = find_neighbor_status(CG, schema)
        schema, cumulative_df = calculate_changes(neighbor_obj, schema, cumulative_df, month_tracker, run_mode)
        month_tracker += 1

    return cumulative_df


def make_starting_df(schema):
    county_list = list(schema[county].name for county in schema)
    starting_infestation = list(schema[county].infestation for county in schema)
    cumulative_df = pd.DataFrame({'County': county_list})
    cumulative_df.insert(1, f'month 0', starting_infestation, True)
    return cumulative_df


def find_neighbor_status(CG, schema):
    """
    Ascertains the infestation status of all neighbors for each county instance,
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


def calculate_changes(neighbor_obj, schema, cumulative_df, month_tracker, run_mode):
    """
    SUPER TENTATIVE
    This iterates outcomes of month interactions randomly
    :param neighbor_obj:
    :param schema:
    :return:

    TODO: Figure out how to model the actual math here.
    TODO: Establish run modes
    """

    # print('------------------------- Begin New month -------------------------')
    if run_mode == 'Baseline':
        schema, cumulative_df = baseline_calc(neighbor_obj, schema, cumulative_df, month_tracker)
    elif run_mode == 'Poison ToH':
        schema, cumulative_df = ToH_calc(neighbor_obj, schema, cumulative_df, month_tracker)
    elif run_mode == 'Population-Based Countermeasures':
        schema, cumulative_df = population_calc(neighbor_obj, schema, cumulative_df, month_tracker)
    elif run_mode == 'Quarantine':
        schema, cumulative_df = quarantine_calc(neighbor_obj, schema, cumulative_df, month_tracker)
    return schema, cumulative_df


def baseline_calc(neighbor_obj, schema, cumulative_df, month_tracker):
    """

    :param neighbor_obj:
    :param schema:
    :param cumulative_df:
    :param month_tracker:
    :return:
    """
    infestation_collector = []
    for county_net in neighbor_obj:
        all_new_infestations = 0
        county = get_object(county_net, schema)
        county.infestation = county.infestation + (county.infestation * random.normal(0.025, 0.01))
        for net_neighbors in neighbor_obj[county_net]:
            probability = random.normal(0.5, 0.8)  # random.normal(loc= , scale= )  # SAMPLE EQUATION
            ToH_modifier = (net_neighbors.infestation ** 2
                            * net_neighbors.toh_density_percentile
                            * random.exponential(0.02))
            new_infestation = ((net_neighbors.infestation * probability) +
                               (ToH_modifier * net_neighbors.infestation))
            all_new_infestations += new_infestation
        all_new_infestations = round(all_new_infestations / (len(neighbor_obj[county_net])), 8) + county.infestation
        if all_new_infestations > 1:
            all_new_infestations = 1
        if all_new_infestations < 0:
            all_new_infestations = 0
        # print(f'{county_net} went from {county.infestation} to {all_new_infestations}')
        setattr(county, 'infestation', all_new_infestations)
        infestation_collector.append(all_new_infestations)
    cumulative_df.insert(month_tracker + 1, f'month {month_tracker}', infestation_collector, True)
    return schema, cumulative_df


def ToH_calc(neighbor_obj, schema, cumulative_df, month_tracker):
    """
    Since ToH are a food source for SLF,
    this block of code models the efficacy of targeting ToH instead of SLF directly
    :param neighbor_obj:
    :param schema:
    :param cumulative_df:
    :param month_tracker:
    :return:
    """
    infestation_collector = []
    for county_net in neighbor_obj:
        all_new_infestations = 0
        county = get_object(county_net, schema)
        county.infestation = county.infestation + (county.infestation * random.normal(0.025, 0.01))
        for net_neighbors in neighbor_obj[county_net]:
            probability = random.normal(0.5, 0.8)  # random.normal(loc= , scale= )  # SAMPLE EQUATION
            ToH_modifier = (net_neighbors.infestation ** 2
                            * net_neighbors.toh_density_percentile
                            * random.exponential(0.02)
                            * -1)
            new_infestation = net_neighbors.infestation * probability + ToH_modifier * net_neighbors.infestation
            all_new_infestations += new_infestation
        all_new_infestations = round(all_new_infestations / (len(neighbor_obj[county_net])), 8) + county.infestation
        if all_new_infestations > 1:
            all_new_infestations = 1
        if all_new_infestations < 0:
            all_new_infestations = 0
        # print(f'{county_net} went from {county.infestation} to {all_new_infestations}')
        setattr(county, 'infestation', all_new_infestations)
        infestation_collector.append(all_new_infestations)
    cumulative_df.insert(month_tracker + 1, f'month {month_tracker}', infestation_collector, True)
    return schema, cumulative_df


def population_calc(neighbor_obj, schema, cumulative_df, month_tracker):
    """
    Mimics what happens when a popoulation in a county is instructed to destroy SLF and eggs
    Uses population density to approximate the intervention
    :param neighbor_obj:
    :param schema:
    :param cumulative_df:
    :param month_tracker:
    :return:
    """
    infestation_collector = []
    for county_net in neighbor_obj:
        all_new_infestations = 0
        county = get_object(county_net, schema)
        county.infestation = county.infestation + (county.infestation * random.normal(0.025, 0.01))
        for net_neighbors in neighbor_obj[county_net]:
            probability = random.normal(0.5, 0.8)  # random.normal(loc= , scale= )  # SAMPLE EQUATION
            bug_smash = random.normal(0.3, 0.1) * 0.01
            ToH_modifier = (net_neighbors.infestation ** 2
                            * net_neighbors.toh_density_percentile
                            * random.exponential(0.02))
            # print((1/net_neighbors.popdense_sqmi) * county.infestation)
            new_infestation = (net_neighbors.infestation * probability +
                               ToH_modifier * net_neighbors.infestation -
                               (county.infestation * net_neighbors.popdense_sqmi * bug_smash))
            all_new_infestations += new_infestation
        all_new_infestations = round(all_new_infestations / (len(neighbor_obj[county_net])), 8) + county.infestation
        if all_new_infestations > 1:
            all_new_infestations = 1
        if all_new_infestations < 0:
            all_new_infestations = 0
        # print(f'{county_net} went from {county.infestation} to {all_new_infestations}')
        setattr(county, 'infestation', all_new_infestations)
        infestation_collector.append(all_new_infestations)
    cumulative_df.insert(month_tracker + 1, f'month {month_tracker}', infestation_collector, True)
    return schema, cumulative_df


def quarantine_calc(neighbor_obj, schema, cumulative_df, month_tracker):
    infestation_collector = []
    quarantine_list = set()  # actually this is fine where it is
    for county_net in neighbor_obj:
        all_new_infestations = 0
        county = get_object(county_net, schema)
        county.infestation = county.infestation + (county.infestation * random.normal(0.025, 0.01))
        for net_neighbors in neighbor_obj[county_net]:
            if (net_neighbors in quarantine_list) or (net_neighbors.infestation > 0.5 and random.choice([True, False])):
                new_infestation = 0
                quarantine_list.add(net_neighbors)
            else:
                probability = random.normal(0.5, 0.8)
                ToH_modifier = (net_neighbors.infestation ** 2
                                * net_neighbors.toh_density_percentile
                                * random.exponential(0.02))
                new_infestation = net_neighbors.infestation * probability + ToH_modifier * net_neighbors.infestation

            all_new_infestations += new_infestation
        all_new_infestations = round(all_new_infestations / (len(neighbor_obj[county_net])), 8) + county.infestation
        if all_new_infestations > 1:
            all_new_infestations = 1
        if all_new_infestations < 0:
            all_new_infestations = 0
        # print(f'{county_net} went from {county.infestation} to {all_new_infestations}')
        setattr(county, 'infestation', all_new_infestations)
        infestation_collector.append(all_new_infestations)
    cumulative_df.insert(month_tracker + 1, f'month {month_tracker}', infestation_collector, True)
    return schema, cumulative_df


if __name__ == '__main__':
    infestation_main('Population-Based Countermeasures', 10)
