"""
File name: threepg_species_data.py
Author: Grace Todd
Date: May 08, 2024
Description: Holds the SpeciesData class, which will be used to manipulate common parameters
	for each of the species used in a simulation.
"""

import csv

class SpeciesData:
    def __init__(self, name, name_scientific, q_leaf_shape, q_canopy_density, q_deciduous_evergreen, q_leaf_color, q_tree_form, q_tree_roots, q_habitat, q_bark_texture, q_bark_color, t_min=0, t_opt=0, t_max=0, kf=0, fcax_700=0, kd=0, n_theta=0, c_theta=0, p2=0, p20=0, acx=0, sla_1=0, sla_0=0, t_sla_mid=0, fn0=0, nfn=0, tc=0, max_age=0, r_age=0, n_age=0, mf=0, mr=0, ms=0, yfx=0, yf0=0, tyf=0, yr=0, nr_max=0, nr_min=0, m_0=0, wsx1000=0, nm=0, k=0, aws=0, nws=0, ah=0, nhb=0, nhc=0, ahl=0, nhlb=0, nhlc=0, ak=0, nkb=0, nkh=0, av=0, nvb=0, nvh=0, nvbh=0, ):
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


def parse_csv_file(file_path):
    # Parses a CSV file output from NLP into Tree and TreeList objects # Needs to be updated as more attributes for trees are included
    # Common_name,scientific_name,leaf_shape_(oval/truncate/elliptical/lancolate/linear/other),
    #canopy_density_(very_thin/thin/medium/dense/very_dense),deciduous_or_evergreen,
    #leaf_color_(green),tree_form_(round/spreading/pyramidal/oval/conical/vase/columnar/open/weeping/irregular),
    #tree_roots_(deep/shallow),habitat_(polar/temperate/dry/continental/tropical/subtropical/subcontinental/
    #mediterranean/alpine/arid/subarctic/subalpine),bark_texture_(smooth/lenticels/furrows/ridges/cracks/scales/strips),
    #bark_color_(gray/white/red/brown)
    trees = []
    # read in the tree params
    tree_params = csv_file_to_list(file_path)
    print(f"tree_params: {tree_params}")

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # read in the tree_params and assign the value at row[param] for param in tree_params
            name = row['Common_name']
            name_scientific = row['scientific_name']
            leaf_shape = row['leaf_shape_(oval/truncate/elliptical/lancolate/linear/other)']
            canopy_density = row['canopy_density_(very_thin/thin/medium/dense/very_dense)']
            deciduous_evergreen = row['deciduous_or_evergreen']
            leaf_color = row['leaf_color_(green)']
            tree_form= row['tree_form_(round/spreading/pyramidal/oval/conical/vase/columnar/open/weeping/irregular)']
            tree_roots = row['tree_roots_(deep/shallow)']
            habitat = row['habitat_(polar/temperate/dry/continental/tropical/subtropical/subcontinental/mediterranean/alpine/arid/subarctic/subalpine)']
            bark_texture = row['bark_texture_(smooth/lenticels/furrows/ridges/cracks/scales/strips)']
            bark_color = row['bark_color_(gray/white/red/brown)']
            tree = SpeciesData(name, name_scientific, leaf_shape, canopy_density, deciduous_evergreen, leaf_color, tree_form, tree_roots, habitat, bark_texture, bark_color)
            trees.append(tree)

    return trees

def csv_file_to_list(file_path):
    attribute_list = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Exclude lines starting with a comment character (e.g., #)
            if not row or row[0].startswith("#"):
                continue
            attribute_list.append(row)
    return attribute_list
# Example usage:
#species_csv = "test_data/douglas_fir_species_data.csv"
#species = parse_species_data(species_csv)
#for tree in species:
    #tree.print_species_data()
