"""
File name: test_threepg.py
Author: Grace Todd
Date: February 28, 2024
Description: This file tests out the 3-PG implementation in threepg.py using Douglas Fir species data.
             Before I start working on the data estimation agent, I need to make sure that the trees
             are actually growing/dying how I expect them to be.
"""

from threepg import compute, TreeViz
from plot_trees_random import init_trees

speciesdata_filename = 'test_data/douglas_fir_species_data.csv'
climatedata_filename = 'test_data/sample_climate_data.csv'  # Create this