# create_classes.py

"""
This file will contain the classes to be used in the MC simualtion
"""

from numpy import random


class Location:
    def __init__(self, lat, lng, ToH_density, OT_density, quarantine):
        self.lat = lat
        self.lng = lng
        self.ToH_density = ToH_density  # "tree of heaven density"
        self.OT_density = OT_density  # "Other trees density"
        self.quarantine = quarantine


class City(Location):
    def __init__(self, lat, lng, ToH_density, OT_density, quarantine, population):
        super().__init__(lat, lng, ToH_density, OT_density, quarantine)
        self.population = population


class Vehicle:
    def __init__(self, size):
        self.size = size


class Truck(Vehicle):
    def __init__(self, size, infection_prob):
        super().__init__(self, size)
        self.avg_dist_per_day = float(random.normal(loc=500, scale=1)) # in miles
        self.infection_prob = infection_prob

    def make_trip(self, size, infection_prob):
        infect_rand = float(random.normal(loc=0, scale=1))
        if infect_rand >= 0:
            self.infection_prob = size * infect_rand * 0.001
        else:
            self.infection_prob = 0
        return infection_prob


class Train(Vehicle):
    def __init__(self, size):
        super().__init__(self, size)
        self.infection_prob = 0.2  # placeholder likelihood of infection.
        self.avg_dist_per_day = float(random.normal(loc=600, scale=1))  # in miles