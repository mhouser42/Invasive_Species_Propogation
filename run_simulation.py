import pickle
from numpy import random
import pandas as pd


def invasion_main():
    """
    Main Function that sequences the order of events when running this file
    :return:
    """
    CG, schema = set_up()
    schema = set_coefficients(schema)
    cumulative_df = week(CG, schema)
    print(cumulative_df)


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
    :param schema:
    :return:
    """
    coef_dict = { # This is where we can adjust parameters. Should we save this in an exported JSON?
                 'Cook': {'infection': 0.1},  # The idea was to set up a dict we could use for all attributes we want
                 'DuPage': {'infection': 0},
                 'Kane': {'infection': 0.3},
                 'Will': {'infection': 0},
                 'Winnebago': {'infection': 0},
                 'Lake': {'infection': 0},
                 'McHenry': {'infection': 0},
                 'St. Clair': {'infection': 0},
                 'Kendall': {'infection': 0},
                 'Madison': {'infection': 0.5},
                 'Rock Island': {'infection': 0},
                 'Peoria': {'infection': 0},
                 'Sangamon': {'infection': 0},
                 'Tazewell': {'infection': 0},
                 'Champaign': {'infection': 0.8},
                 'Boone': {'infection': 0},
                 'Macon': {'infection': 0},
                 'Kankakee': {'infection': 0},
                 'DeKalb': {'infection': 0},
                 'Williamson': {'infection': 0},
                 'McLean': {'infection': 0},
                 'Grundy': {'infection': 0.1},
                 'Coles': {'infection': 0},
                 'Jackson': {'infection': 0},
                 'LaSalle': {'infection': 0},
                 'Franklin': {'infection': 0},
                 'Vermilion': {'infection': 0},
                 'Monroe': {'infection': 0},
                 'Stephenson': {'infection': 0.6},
                 'Whiteside': {'infection': 0},
                 'Adams': {'infection': 0},
                 'Clinton': {'infection': 0},
                 'Knox': {'infection': 0},
                 'Woodford': {'infection': 0},
                 'Effingham': {'infection': 0},
                 'Ogle': {'infection': 0.3},
                 'Marion': {'infection': 0},
                 'Jefferson': {'infection': 0},
                 'Saline': {'infection': 0},
                 'Massac': {'infection': 0},
                 'Morgan': {'infection': 0},
                 'Henry': {'infection': 0},
                 'Jersey': {'infection': 0},
                 'Randolph': {'infection': 0},
                 'McDonough': {'infection': 0},
                 'Macoupin': {'infection': 0},
                 'Wabash': {'infection': 0},
                 'Perry': {'infection': 0},
                 'Logan': {'infection': 0},
                 'Lee': {'infection': 0},
                 'Christian': {'infection': 0},
                 'Douglas': {'infection': 0},
                 'Bond': {'infection': 0},
                 'Lawrence': {'infection': 0},
                 'Richland': {'infection': 0},
                 'Crawford': {'infection': 0},
                 'Moultrie': {'infection': 0},
                 'Montgomery': {'infection': 0},
                 'Union': {'infection': 0},
                 'Fulton': {'infection': 0},
                 'DeWitt': {'infection': 0},
                 'Menard': {'infection': 0},
                 'Bureau': {'infection': 0},
                 'Piatt': {'infection': 0},
                 'Livingston': {'infection': 0},
                 'Johnson': {'infection': 0},
                 'Jo Daviess': {'infection': 0},
                 'Cass': {'infection': 0},
                 'Putnam': {'infection': 0},
                 'Warren': {'infection': 0},
                 'Carroll': {'infection': 0},
                 'Clark': {'infection': 0},
                 'Cumberland': {'infection': 0},
                 'Alexander': {'infection': 0},
                 'Marshall': {'infection': 0},
                 'Fayette': {'infection': 0},
                 'Edwards': {'infection': 0},
                 'Pulaski': {'infection': 0},
                 'Clay': {'infection': 0},
                 'Edgar': {'infection': 0},
                 'White': {'infection': 0},
                 'Shelby': {'infection': 0},
                 'Ford': {'infection': 0},
                 'Mercer': {'infection': 0},
                 'Iroquois': {'infection': 0},
                 'Washington': {'infection': 0},
                 'Mason': {'infection': 0},
                 'Greene': {'infection': 0},
                 'Hardin': {'infection': 0},
                 'Wayne': {'infection': 0},
                 'Hancock': {'infection': 0},
                 'Brown': {'infection': 0},
                 'Scott': {'infection': 0},
                 'Stark': {'infection': 0},
                 'Jasper': {'infection': 0},
                 'Hamilton': {'infection': 0},
                 'Pike': {'infection': 0},
                 'Henderson': {'infection': 0},
                 'Calhoun': {'infection': 0},
                 'Schuyler': {'infection': 0},
                 'Gallatin': {'infection': 0},
                 'Pope': {'infection': 0}
                    }
    for coef_county in coef_dict:
        for attribute in coef_dict[coef_county]:
            setattr(schema[coef_county], attribute, coef_dict[coef_county][attribute])
    return schema


def week(CG, schema):
    """
    Takes the initial schema and iterates it through a number of weeks
    :param CG:
    :param schema:
    :return:
    """
    weeks = input('How many weeks are you running? \n')
    cumulative_df = make_starting_df(schema)
    week_tracker = 1
    for i in range(0, int(weeks)):
        neighbor_obj = find_neighbor_status(CG, schema)
        schema, cumulative_df = calculate_changes(neighbor_obj, schema, cumulative_df, week_tracker)
        week_tracker += 1

    return cumulative_df


def make_starting_df(schema):
    # cumulative_df = pd.DataFrame(['Cook',
    #                               'DuPage',
    #                               'Kane',
    #                               'Will',
    #                               'Winnebago',
    #                               'Lake',
    #                               'McHenry',
    #                               'St. Clair',
    #                               'Kendall',
    #                               'Madison',
    #                               'Rock Island',
    #                               'Peoria',
    #                               'Sangamon',
    #                               'Tazewell',
    #                               'Champaign',
    #                               'Boone',
    #                               'Macon',
    #                               'Kankakee',
    #                               'DeKalb',
    #                               'Williamson',
    #                               'McLean',
    #                               'Grundy',
    #                               'Coles',
    #                               'Jackson',
    #                               'LaSalle',
    #                               'Franklin',
    #                               'Vermilion',
    #                               'Monroe',
    #                               'Stephenson',
    #                               'Whiteside',
    #                               'Adams',
    #                               'Clinton',
    #                               'Knox',
    #                               'Woodford',
    #                               'Effingham',
    #                               'Ogle',
    #                               'Marion',
    #                               'Jefferson',
    #                               'Saline',
    #                               'Massac',
    #                               'Morgan',
    #                               'Henry',
    #                               'Jersey',
    #                               'Randolph',
    #                               'McDonough',
    #                               'Macoupin',
    #                               'Wabash',
    #                               'Perry',
    #                               'Logan',
    #                               'Lee',
    #                               'Christian',
    #                               'Douglas',
    #                               'Bond',
    #                               'Lawrence',
    #                               'Richland',
    #                               'Crawford',
    #                               'Moultrie',
    #                               'Montgomery',
    #                               'Union',
    #                               'Fulton',
    #                               'DeWitt',
    #                               'Menard',
    #                               'Bureau',
    #                               'Piatt',
    #                               'Livingston',
    #                               'Johnson',
    #                               'Jo Daviess',
    #                               'Cass',
    #                               'Putnam',
    #                               'Warren',
    #                               'Carroll',
    #                               'Clark',
    #                               'Cumberland',
    #                               'Alexander',
    #                               'Marshall',
    #                               'Fayette',
    #                               'Edwards',
    #                               'Pulaski',
    #                               'Clay',
    #                               'Edgar',
    #                               'White',
    #                               'Shelby',
    #                               'Ford',
    #                               'Mercer',
    #                               'Iroquois',
    #                               'Washington',
    #                               'Mason',
    #                               'Greene',
    #                               'Hardin',
    #                               'Wayne',
    #                               'Hancock',
    #                               'Brown',
    #                               'Scott',
    #                               'Stark',
    #                               'Jasper',
    #                               'Hamilton',
    #                               'Pike',
    #                               'Henderson',
    #                               'Calhoun',
    #                               'Schuyler',
    #                               'Gallatin',
    #                               'Pope'])
    county_list = list(schema[county].name for county in schema)
    starting_infection = list(schema[county].infection for county in schema)
    cumulative_df = pd.DataFrame({'County': county_list})
    cumulative_df.insert(1, f'Week 0', starting_infection, True)
    return cumulative_df


def find_neighbor_status(CG, schema):
    """
    Ascertains the infection status of all neighbors for each county instance,
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


def get_object(name, schema):
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


def calculate_changes(neighbor_obj, schema, cumulative_df, week_tracker):
    """
    SUPER TENTATIVE
    This iterates outcomes of week interactions randomly
    :param neighbor_obj:
    :param schema:
    :return:

    TODO: Figure out how to model the actual math here.
    """

    # print('------------------------- Begin New Week -------------------------')
    infection_collector = []
    for county_net in neighbor_obj:
        all_new_infections = 0
        county = get_object(county_net, schema)
        for net_neighbors in neighbor_obj[county_net]:
            probability = random.normal(0.5, 0.17)  # random.normal(loc= , scale= )
            new_infection = (county.infection + (net_neighbors.infection * probability))/2  # SAMPLE EQUATION
            all_new_infections += new_infection
        all_new_infections = round(all_new_infections / (len(neighbor_obj[county_net])), 8)
        if all_new_infections > 1:  #
            all_new_infections = 1
        # print(f'{county_net} went from {county.infection} to {all_new_infections}')
        # setattr(county, 'infection', all_new_infections)
        infection_collector.append(all_new_infections)
    cumulative_df.insert(week_tracker + 1, f'Week {week_tracker}', infection_collector, True)
    return schema, cumulative_df


if __name__ == '__main__':
    invasion_main()