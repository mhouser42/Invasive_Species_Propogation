# my_classes.py

"""
This file will contain the classes to be used in the MC simulation
"""

from numpy import random
import pandas as pd
import pickle




class Location:

    def __init__(self, name, infection=None, lat=None, lon=None, geometry=None, bbox_n=None, bbox_s=None,
                 bbox_e=None, bbox_w=None, pop=None, popdense_sqmi=None, slf_count=None, egg_count=None,
                 ToH_density=None, quarantine=False, centroid=False):
        self.name = name
        self.lat, self.lon, self.geometry = lat, lon, geometry
        self.bbox_n, self.bbox_s, self.bbox_e, self.bbox_w = bbox_n, bbox_s, bbox_e, bbox_w
        self.pop, self.popdense_sqmi = pop, popdense_sqmi
        self.egg_count = egg_count
        self.slf_count = slf_count
        self.quarantine = quarantine
        self.centroid = centroid
        self.infection = 0

        # CG = pickle.load(open('data/location/IL_graph.dat', 'rb'))
        # self.neighbors = [neighbor.name for neighbor in CG.neighbors(name)]

    def get_neighbor_objects(self, graph):
        for node in graph.nodes():
            if hasattr(node, 'name') and node.name == self.name:
                return[neighbor for neighbor in graph.neighbors(node)]
        return []

    def get_my_object(self, graph):
        node_list = []
        for node in graph.nodes():
            if hasattr(node, 'name') and node.name == self.name:
                node_list.append(node)
        return node

    def __hash__(self):
        return hash((self.name, type(self)))

    def __eq__(self, other):
        return self.name == other.name and type(self) == type(other)

    # def update_week(self):
    #     CG = pickle.load(open(f'data/location/IL_graph.dat', 'rb'))
    #     return neighbors


class County(Location):
    def __init__(self, name, toh_density=None, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.toh_density = toh_density
        _ToH_density_list = []

    def track_ToH_density(self):
        self._ToH_density_list = self._ToH_density_list.append(self.ToH_density)
        return self._ToH_density_list

    def ToH_killing_OT(self):
        if self._ToH_density_list[-1] > self._ToH_density_list[-2]:
            self.OT_density = self.OT_density - (_ToH_density_list[-1] - _ToH_density_list[-2])
        return self.OT_density

    def deforrestation(self):
        return self.ToH_density/2


class City(Location):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)


class Vehicle:
    def __init__(self, infection_prob, avg_dist_per_day, avg_range):
        self.avg_dist_per_day = avg_dist_per_day
        self.infection_prob = infection_prob
        self.avg_range = avg_range
    def avg_dist(self):
        self.avg_dist_per_day = float(random.normal(loc=self.avg_range, scale=1))  # in miles
        return self.avg_dist_per_day
    def make_trip(self):
        self.infect_rand = float(random.normal(loc=0, scale=1))
        if self.infect_rand > 0:
            self.infection_prob =self.infect_rand * 0.01
        else:
            self.infection_prob = 0
        return self.infection_prob


class Truck(Vehicle):
    def __init__(self, infection_prob, avg_dist_per_day):
        Vehicle.__init__(self, infection_prob, avg_dist_per_day, 500)


class Train(Vehicle):
    def __init__(self, infection_prob, avg_dist_per_day):
        Vehicle.__init__(self, infection_prob, avg_dist_per_day, 600)


class Insect:
    def __init__(self, age, hunger, oldest):
        self.age = age
        self.hunger = hunger
        self.oldest = oldest

    def ageing(self):
        self.age += 1
        if self.age > self.oldest:
            del self

    def print_status(self):
        print(f'I am {self.age} weeks old,\n'
              f'My hunger level is {self.hunger}\n'
              f'I live to be {self.oldest}.')


class SLF(Insect):
    def __init__(self, age, hunger, oldest):
        super().__init__(age, hunger, oldest)
        self.oldest = 8
        self._kid_counter = 0
    def seek_food(self):
        if self.hunger >= 10:
            # Prioritize heading towards areas with trees over laying eggs
            pass

    def propagate(self):
        if (self.age >= 3) and (self.hunger <= 6) and (random.choice([0, 1]) > 0):
            # SLF(0, 0, 8)
            self._kid_counter += 1
            print('made a kid!')
        return self._kid_counter

    def print_status(self):
        print(f'I am {self.age} weeks old,\n'
              f' My hunger level is {self.hunger},\n'
              f' and I have made {self._kid_counter} kids.')

class Wasp(Insect):
    def __init__(self, age, hunger):
        Insect.__init__(age, hunger, 5)


    def hunt(self):
        if self.hunger >= 10:
            # Prioritize hunting SLF
            pass
        # for  # SLF killed
            Wasp(0, 0)