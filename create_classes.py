# create_classes.py

"""
This file will contain the classes to be used in the MC simualtion
"""


class Location:
    def __init__(self, lat, lng, ToH_density, OT_density):
        self.lat = lat
        self.lng = lng
        self.ToH_density = ToH_density  # "tree of heaven density"
        self.OT_density = OT_density  # "Other trees density"


class City(Location):
    def __init__(self, lat, lng, ToH_density, OT_density, population):
        super().__init__(lat, lng, ToH_density, OT_density)
        self.population = population


class Vehicle:
    def __init__(self, size, commercial):
        self.size = size
        self.commercial = commercial


class Truck(Vehicle):
    def __init__(self):
        pass


class Train(Vehicle):
    def __init__(self):
        pass