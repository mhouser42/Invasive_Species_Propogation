# my_classes.py

"""
This file will contain the classes to be used in the MC simulation

TODO: Write documentation for the code in this file
"""

from queue import Queue
from numpy import random


class County:
    """
    Hashable object with various attributes related to lanternfly infestation and geographical data.

    :param name: Name of the location.
    :param lat: Latitude coordinate.
    :param lon: Longitude coordinate.
    :param geometry: Geometrical data of the location.
    :param centroid: Centroid of the location (if available).
    :param pop: Population of the location.
    :param popdense_sqmi: Population density per square mile.
    :param infestation: Initial infestation level.
    :param mated: Proportion of the infestation that has mated.
    :param laid_eggs: Proportion of the infestation that has laid eggs.
    :param egg_count: Number of egg masses present.
    :param quarantine: Boolean indicating if the location is under quarantine.
    """

    def __init__(self, name, lat=None, lon=None, geometry=None, centroid=False, pop=None, popdense_sqmi=None,
                 infestation=0.0, mated=0.0, laid_eggs=0.0, egg_count=0,
                 tree_density=0.0, toh_density=0.0, traffic_level=1.0, quarantine=False):
        self.name = name
        self.lat, self.lon, self.geometry, self.centroid = lat, lon, geometry, centroid
        self.pop, self.popdense_sqmi = pop, popdense_sqmi
        self.infestation = infestation
        self.mated = mated
        self.laid_eggs = laid_eggs
        self.egg_count = egg_count
        self.tree_density = tree_density
        self.toh_density = toh_density
        self.traffic_level = traffic_level
        self.quarantine = quarantine

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

    def mate(self, mating_chance=None):
        """
        Simulate the mating process, updating the proportion of mated flies in the infestation

        >>> county = County('Butts County', infestation=0.7)
        >>> old_mate = county.mate()
        >>> new_mate = county.mate()
        >>> new_mate > old_mate
        True
        """
        if mating_chance is None:
            mating_chance = random.uniform(0.5, 1.0)
        newly_mated = self.infestation * mating_chance * (1.0 - self.mated)
        self.mated += newly_mated
        self.mated = min(self.mated, 1.0)  # caps the value at 100%
        return self.mated

    def lay_eggs(self, scaling_factor=100, extra_eggmass_chance=0.05):
        """
        Simulates the laying of eggs based on the porportion of mated SLFs.

        :param scaling_factor: Factor to convert mated proportion to number of egg masses.
        :param extra_eggmass_chance: Chance of laying an additional egg mass.
        :return self.eggcount: Total number of egg masses after laying.

        >>> loc = County("Matt's County", infestation=0.37, mated=1.0)
        >>> current_eggs = loc.lay_eggs()
        105
        """
        new_egg_masses = int(self.mated * scaling_factor)
        additional_egg_masses = int(new_egg_masses * extra_eggmass_chance)
        self.egg_count += new_egg_masses + additional_egg_masses
        return self.egg_count

    def die_off(self, mortality_rate=None):
        """
        Simulates the natural death of SLF during the winter.
        :return self.infestation: current infestation level of Location
        """
        if mortality_rate is None:
            mortality_rate = random.uniform(.80, .90)
        die_off_number = int(self.infestation * mortality_rate)
        self.infestation -= die_off_number
        self.mated = 0.0
        self.laid_eggs = 0.0
        return self.infestation

    def hatch_eggs(self, hatch_chance=None):
        """
        Simulates the hatching of eggs and increases the infestation accordingly.

        :return: infestation level after hatching eggs.

        >>> loc = County("Cook", infestation=0.0, egg_count=105)
        >>> pre_hatch_infestation = loc.infestation
        >>> current_infest = loc.hatch_eggs(hatch_chance=1.0)
        >>> current_infest > 0.37
        True

        """
        if hatch_chance is None:
            hatch_chance = random.uniform(.75, 1.0)
        hatched_eggs = int(self.egg_count * hatch_chance)
        while hatched_eggs > 0:
            egg_coef = random.uniform(0.0035, 0.0045)
            self.infestation += egg_coef
            self.egg_count -= 1
            hatched_eggs -= 1

        self.infestation = min(self.infestation, 1.0)  # caps at 100%
        return self.infestation

    def __hash__(self):
        return hash((self.name, type(self)))

    def __eq__(self, other):
        return self.name == other.name and type(self) == type(other)


class MonthQueue(Queue):
    def __init__(self):
        super().__init__()
        self.months_traffic_levels = {
            'January': 0.9, 'February': 0.9, 'March': 0.92, 'April': 0.94,
            'May': 0.96, 'June': 0.98, 'July': 1.0, 'August': 0.98,
            'September': 0.96, 'October': 0.94, 'November': 0.92, 'December': 0.90
        }
        for month, traffic_level in self.months_traffic_levels.items():
            self.put((month, traffic_level))

    def rotate(self):
        old_month = self.get()
        self.put(old_month)
        return old_month

    def get_traffic_level(self, month):
        return self.months_traffic_levels[month]


# class County(Location):
#     def __init__(self, name, toh_density_percentile=None, *args, **kwargs):
#         super().__init__(name, *args, **kwargs)
#         self.toh_density_percentile = toh_density_percentile
#         _ToH_density_list = []
#
#     def track_ToH_density(self):
#         self._ToH_density_list = self._ToH_density_list.append(self.toh_density_percentile)
#         return self._ToH_density_list
#
#     def deforestation(self):
#         return self.ToH_density / 2
#
#
# class City(Location):
#     def __init__(self, name, *args, **kwargs):
#         super().__init__(name, *args, **kwargs)
