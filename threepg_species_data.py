"""
File name: threepg_species_data.py
Author: Grace Todd
Date: April 30, 2024
Description: Holds the SpeciesData class, which will be used to manipulate common parameters
	for each of the species used in a simulation.
"""

from parse_tree_input import csv_file_to_list

class SpeciesData:
    def __init__(self, name,q_leaf_shape,q_canopy_density,q_deciduous_evergreen,q_leaf_color,q_tree_form,q_tree_roots,q_habitat,q_bark_texture,q_bark_color,t_min=None,t_opt=None,t_max=None,df=None,kf=None,fcax_700=None,kd=None,soil_water=None,max_soil_water=None,n_theta=None,c_theta=None,lec=None,p2=None,p20=None,acx=None,sla_1=None,sla_0=None,t_sla_mid=None,fn0=None,nfn=None,tc=None,max_age=None,r_age=None,n_age=None,mf=None,mr=None,ms=None,yfx=None,yf0=None,tyf=None,yr=None,nr_min=None,nr_max=None,m_0=None,wsx1000=None,nm=None,k=None,aws=None,nws=None,ah=None,nhb=None,nhc=None,ahl=None,nhlb=None,nhlc=None,ak=None,nkb=None,nkh=None,av=None,nvb=None,nvh=None,nvbh=None,):
        """
        Initializes the SpeciesData class with the provided attributes.
        """
        self.name = name
        self.q_leaf_shape = q_leaf_shape.split('/')
        self.q_leaf_shape = q_leaf_shape
        self.q_canopy_density = q_canopy_density.split('/')
        self.q_canopy_density = q_canopy_density
        self.q_deciduous_evergreen = q_deciduous_evergreen.split('/')
        self.q_deciduous_evergreen = q_deciduous_evergreen
        self.q_leaf_color = q_leaf_color.split('/')
        self.q_leaf_color = q_leaf_color
        self.q_tree_form = q_tree_form.split('/')
        self.q_tree_form = q_tree_form
        self.q_tree_roots = q_tree_roots.split('/')
        self.q_tree_roots = q_tree_roots
        self.q_habitat = q_habitat.split('/')
        self.q_habitat = q_habitat
        self.q_bark_texture = q_bark_texture.split('/')
        self.q_bark_texture = q_bark_texture
        self.q_bark_color = q_bark_color.split('/')
        self.q_bark_color = q_bark_color
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
        self.sla_0 = sla_0
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
        self.aws = aws
        self.nws = nws
        self.ah = ah
        self.nhb = nhb
        self.nhc = nhc
        self.ahl = ahl
git         self.nhlb = nhlb
        self.nhlc = nhlc
        self.ak = ak
        self.nkb = nkb
        self.nkh = nkh
        self.av = av
        self.nvb = nvb
        self.nvh = nvh
        self.nvbh = nvbh

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
species_csv = "test_data/douglas_fir_species_data.csv"
species = parse_species_data(species_csv)
for tree in species:
    tree.print_species_data()
