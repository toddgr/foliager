"""
File name: threepg_env_data.py
Author: Grace Todd
Date: May 03, 2024
Description: Holds the Environment class, which will be used to manipulate common parameters
	for the environment used in a simulation.
"""

from parse_tree_input import csv_file_to_list

class Environment:
    def __init__(self, tmax=None, tmin=None, rain=None, solar_rad=None, frost_days=None, soil_water=None, max_soil_water=None, ):
        """
        Initializes the Environment class with the provided attributes.
        """
        self.tmax = float(tmax)
        self.tmin = float(tmin)
        self.rain = float(rain)
        self.solar_rad = float(solar_rad)
        self.frost_days = float(frost_days)
        self.soil_water = float(soil_water)
        self.max_soil_water = float(max_soil_water)
