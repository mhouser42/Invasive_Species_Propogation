# create_classes.py

"""
This file will contain the classes to be used in the MC simualtion
"""


class City:
    def __init__(self, population, lat, lng):
        self.population = population
        self.lat = lat
        self.lng = lng
