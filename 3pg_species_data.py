"""
File: 3pg.py
Author: Grace Todd
Date: February 21, 2024
Description: Holds the SpeciesData class, which will be used to manipulate common parameters
            for each of the species used in a simulation.
"""

import csv
from parse_tree_input import csv_file_to_list

class SpeciesData:
    def __init__(self,t_min, t_opt, t_max, df, kf, fcax_700, kd, soil_water, max_soil_water, n_theta, c_theta,\
            lec, p2, p20, acx, sla_1, sla0, t_sla_mid, fn0, nfn, tc, max_age, r_age, n_age, mf, mr, \
            ms, yfx, yf0, tyf, yr, nr_min, nr_max, m_0, wsx1000, nm, k):
        """
            Reads in the CSV of the specific species data,
            and parses it into the class object.
            I don't think we really need anything more than that.

            Actually... I'm going to have foliager generate a CSV of ALL 
            the tree species info, then this will focus on one line at a time.
            TODO Sort through these and add comments for what is what
            TODO need to clean this up or automate generation for it or something, this is super delicate
        """
        self.t_min = t_min
        self.t_opt = t_opt
        self.t_max = t_max
        self.df = df
        self.kf = kf
        self.fcax_700 = fcax_700
        self.kd = kd
        self.soil_water = soil_water
        self.max_soil_water = max_soil_water
        self.n_theta = n_theta
        self.c_theta = c_theta
        self.lec = lec
        self.p2 = p2
        self.p20 = p20
        self.acx = acx
        self.sla_1 = sla_1
        self.sla0 = sla0
        self.t_sla_mid = t_sla_mid
        self.fn0 = fn0
        self.nfn = nfn
        self.tc = tc
        self.max_age = max_age
        self.r_age = r_age
        self.n_age = n_age
        self.mf = mf
        self.mr = mr
        self.ms = ms
        self.yfx = yfx
        self.yf0 = yf0
        self.tyf = tyf
        self.yr = yr
        self.nr_min = nr_min
        self.nr_max = nr_max
        self.m_0 = m_0
        self.wsx1000 = wsx1000
        self.nm = nm
        self.k = k
    
    def print_species_data(self):
        for attr, value in vars(self).items():
            print(f"{attr}: {value}")


def parse_species_data(file_path):
    species_list = csv_file_to_list(file_path)
    species_data_list = []

    for tree_data in species_list:
        species_data_input = []
        for variable_value in tree_data:
            species_data_input.append(variable_value)
        species_instance = SpeciesData(*species_data_input)
        species_data_list.append(species_instance)

    return species_data_list


# test case
species = parse_species_data("test_data/douglas_fir_species_data.csv")
for tree in species:
    tree.print_species_data()