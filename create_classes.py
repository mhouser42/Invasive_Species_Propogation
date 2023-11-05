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
    def __init__(self):


class Truck(Vehicle):
    def __init__(self, infection_prob):
        super().__init__(self)
        self.avg_dist_per_day = float(random.normal(loc=500, scale=1)) # in miles
        self.infection_prob = infection_prob

    def make_trip(self, infection_prob):
        infect_rand = float(random.normal(loc=0, scale=1))
        if infect_rand > 0:
            self.infection_prob = infect_rand * 0.01
        else:
            self.infection_prob = 0
        return infection_prob


class Train(Vehicle):
    def __init__(self, infection_prob):
        super().__init__(self)
        self.avg_dist_per_day = float(random.normal(loc=600, scale=1))  # in miles
        self.infection_prob = infection_prob

    def make_trip(self, infection_prob):
        infect_rand = float(random.normal(loc=0, scale=1))
        if infect_rand > 0:
            self.infection_prob = infect_rand * 0.01
        else:
            self.infection_prob = 0
        return infection_prob


class Insect:
    def __init__(self, age, hunger):
        self.age = age
        self.hunger = hunger


class SLF(Insect):
    def __init__(self, age, hunger):
        super().__init__(self, age, hunger)

    def seek_food(self, hunger):
        if hunger >= 10:
            # Prioritize heading towards areas with trees over laying eggs


    def propagate(self, age):
        if age >= 10:
            #prioritize creating more SLF

    def old_age(self, age):
        if age > 8:
            # delete instance of SLF class


class Wasp(Insect):
    def __init__(self, age, hunger):
        super().__init__(self, age, hunger)


    def hunt(self, hunger):
        if hunger >= 10:
            # Prioritize hunting SLF
        for  # SLF killed
            # create another wasp instance

    def old_age(self, age):
        if age > 8:
            # delete instance of wasp class