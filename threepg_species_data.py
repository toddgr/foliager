"""
File name: threepg_species_data.py
Author: Grace Todd
Date: May 03, 2024
Description: Holds the SpeciesData class, which will be used to manipulate common parameters
	for each of the species used in a simulation.
"""

from parse_tree_input import csv_file_to_list
import csv
from threepg_env_data import Environment

class SpeciesData:
    def __init__(self, name, name_scientific, q_leaf_shape, q_canopy_density, q_deciduous_evergreen, q_leaf_color, q_tree_form, q_tree_roots, q_habitat, q_bark_texture, q_bark_color, t_min=None, t_opt=None, t_max=None, kf=None, fcax_700=None, kd=None, n_theta=None, c_theta=None, p2=None, p20=None, acx=None, sla_1=None, sla_0=None, t_sla_mid=None, fn0=None, nfn=None, tc=None, max_age=None, r_age=None, n_age=None, mf=None, mr=None, ms=None, yfx=None, yf0=None, tyf=None, yr=None, nr_max=None, nr_min=None, m_0=None, wsx1000=None, nm=None, k=None, aws=None, nws=None, ah=None, nhb=None, nhc=None, ahl=None, nhlb=None, nhlc=None, ak=None, nkb=None, nkh=None, av=None, nvb=None, nvh=None, nvbh=None, ):
        """
        Initializes the SpeciesData class with the provided attributes.
        """
        self.name = name
        self.name_scientific = name_scientific
        self.q_leaf_shape = q_leaf_shape.split('/')
        self.q_canopy_density = q_canopy_density.split('/')
        self.q_deciduous_evergreen = q_deciduous_evergreen.split('/')
        self.q_leaf_color = q_leaf_color.split('/')
        self.q_tree_form = q_tree_form.split('/')
        self.q_tree_roots = q_tree_roots.split('/')
        self.q_habitat = q_habitat.split('/')
        self.q_bark_texture = q_bark_texture.split('/')
        self.q_bark_color = q_bark_color.split('/')
        self.t_min = float(t_min)
        self.t_opt = float(t_opt)
        self.t_max = float(t_max)
        self.kf = float(kf)
        self.fcax_700 = float(fcax_700)
        self.kd = float(kd)
        self.n_theta = float(n_theta)
        self.c_theta = float(c_theta)
        self.p2 = float(p2)
        self.p20 = float(p20)
        self.acx = float(acx)
        self.sla_1 = float(sla_1)
        self.sla_0 = float(sla_0)
        self.t_sla_mid = float(t_sla_mid)
        self.fn0 = float(fn0)
        self.nfn = float(nfn)
        self.tc = float(tc)
        self.max_age = float(max_age)
        self.r_age = float(r_age)
        self.n_age = float(n_age)
        self.mf = float(mf)
        self.mr = float(mr)
        self.ms = float(ms)
        self.yfx = float(yfx)
        self.yf0 = float(yf0)
        self.tyf = float(tyf)
        self.yr = float(yr)
        self.nr_max = float(nr_max)
        self.nr_min = float(nr_min)
        self.m_0 = float(m_0)
        self.wsx1000 = float(wsx1000)
        self.nm = float(nm)
        self.k = float(k)
        self.aws = float(aws)
        self.nws = float(nws)
        self.ah = float(ah)
        self.nhb = float(nhb)
        self.nhc = float(nhc)
        self.ahl = float(ahl)
        self.nhlb = float(nhlb)
        self.nhlc = float(nhlc)
        self.ak = float(ak)
        self.nkb = float(nkb)
        self.nkh = float(nkh)
        self.av = float(av)
        self.nvb = float(nvb)
        self.nvh = float(nvh)
        self.nvbh = float(nvbh)

    def print_species_data(self):
        """
        Prints all attributes of the SpeciesData instance.
        """
        for attr, value in vars(self).items():
            print(f"{attr}: {value}")

def get_tree_names(species_data_list):
	# returns a list of the tree names found in the species data CSV.
	tree_names = []
	for tree in species_data_list:
		tree_names.append(tree.name)
	return tree_names

def parse_species_data(file_path):
    species_list = csv_file_to_list(file_path)
    species_data_list = []

    for tree_data in species_list:
        species_instance = SpeciesData(*tree_data)
        species_data_list.append(species_instance)

    return species_data_list


# Example usage:
#species_csv = "test_data/douglas_fir_species_data.csv"
#species = parse_species_data(species_csv)
#for tree in species:
    #tree.print_species_data()
