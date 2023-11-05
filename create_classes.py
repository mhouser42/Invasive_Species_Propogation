# create_classes.py

"""
This file will contain the classes to be used in the MC simulation
"""

from numpy import random


class Location:
    def __init__(self, lat, lng, ToH_density, OT_density, quarantine):
        self.lat = lat
        self.lng = lng
        self.ToH_density = ToH_density # "tree of heaven density"
        self.OT_density = OT_density  # "Other trees density"
        self.quarantine = quarantine

        _ToH_density_list = []

    def track_ToH_density(self, ToH_density, _ToH_density_list):
        _ToH_density_list = _ToH_density_list.append(ToH_density)
        return _ToH_density_list

    def ToH_killing_OT(self, OT_density, _ToH_density_list):
        if _ToH_density_list[-1] > _ToH_density_list[-2]:
            OT_density = OT_density - (_ToH_density_list[-1] - _ToH_density_list[-2])
        return OT_density


    def deforrestation(self, OT_density, ToH_density):
        OT_density = OT_density/2
        ToH_density = ToH_density/2
        return OT_density, ToH_density


class City(Location):
    def __init__(self, lat, lng, ToH_density, OT_density, quarantine, population):
        super().__init__(lat, lng, ToH_density, OT_density, quarantine)
        self.population = population


class Vehicle:
    def __init__(self, infection_prob, avg_dist_per_day, avg_range):
        self.avg_dist_per_day = avg_dist_per_day
        self.infection_prob = infection_prob
        self.avg_range = avg_range
    def avg_dist(self, avg_range):
        avg_dist_per_day = float(random.normal(loc=avg_range, scale=1))  # in miles
        return avg_dist_per_day
    def make_trip(self, infection_prob):
        infect_rand = float(random.normal(loc=0, scale=1))
        if infect_rand > 0:
            self.infection_prob = infect_rand * 0.01
        else:
            self.infection_prob = 0
        return infection_prob


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

    def old_age(self, age, oldest):
        if age > oldest:
            del self


class SLF(Insect):
    def __init__(self, age, hunger):
        Insect.__init__(age, hunger, 8)

    def seek_food(self, hunger):
        if hunger >= 10:
            # Prioritize heading towards areas with trees over laying eggs


    def propagate(self, age, hunger):
        if (age >= 3) and (hunger <= 6) and (random.choice([0, 1]) > 0):
            self.SLF(0, 0)


class Wasp(Insect):
    def __init__(self, age, hunger):
        Insect.__init__(age, hunger, 5)


    def hunt(self, hunger):
        if hunger >= 10:
            # Prioritize hunting SLF
        for  # SLF killed
            self.Wasp(0, 0)