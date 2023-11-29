# my_classes.py

"""
This file will contain the classes to be used in the MC simulation

TODO: Write documentation for the code in this file
"""

from numpy import random
import pandas as pd
import pickle


class Location:
    """

    """
    def __init__(self, name, saturation=None, lat=None, lon=None, geometry=None, bbox_n=None, bbox_s=None,
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
        self.saturation = saturation

    def get_neighbor_objects(self, CG):  # These are used in run_simulation.py
        for node in CG.nodes():
            if hasattr(node, 'name') and node.name == self.name:
                neighbors = [neighbor for neighbor in CG.neighbors(node)]
        return neighbors

    def get_my_object(self, graph):
        node_list = []
        for node in graph.nodes():
            if hasattr(node, 'name') and node.name == self.name:
                node_list.append(node)
        return node

    def die_off(self, mortality_rate=1.0):
        """

        :param mortality_rate:
        :return:
        """
        die_off_number = int(self.slf_count * mortality_rate)
        self.slf_count -= die_off_number
        return die_off_number

    def lay_eggs(self, mating_chance):
        """

        :param mating_chance:
        """
        expect_matings = int(self.slf_count * mating_chance)
        successful_matings = np.random.poisson(expect_matings)
        self.egg_count += successful_matings

    def hatch_eggs(self, hatch_chance):
        hatch_num = random.randint(0, self.egg_count)
        while hatch_num > 0:
            self.slf_count += random.randint(30, 50)
            self.egg_count -= 1
            hatch_num -= 1

    def __hash__(self):
        return hash((self.name, type(self)))

    def __eq__(self, other):
        return self.name == other.name and type(self) == type(other)


class County(Location):
    """

    """
    def __init__(self, name, toh_density_percentile=None, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.toh_density_percentile = toh_density_percentile
        _ToH_density_list = []

    def track_ToH_density(self):
        self._ToH_density_list = self._ToH_density_list.append(self.toh_density_percentile)
        return self._ToH_density_list

    def deforestation(self):
        return self.ToH_density / 2
