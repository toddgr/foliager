"""
File: create_forest.py
Author: Grace Todd
Date: September 10, 2024
Description: Uses 3-PG to calculate various parameters of a tree, which will be used to generate
             each tree in the simulation at every time interval.
             
             Based on real, scientific data, and uses C++ skeleton framework provided by Allison
             Thompson in her thesis here: https://ir.library.oregonstate.edu/concern/honors_college_theses/x920g532g.

             A revised version of 3pg.py

             THE GENERAL IDEA:
             1. Initialize an empty forest
             2. Compute the data for each species of tree found in the forest
             3. Create individual trees from species data & plot them within the forest
             4. Compute spawned/killed trees throughout the simulation
             5. Take the final state of the forest and write to Blender
"""

import csv
import random

"""
=====================================================================
                                CLASSES
=====================================================================
"""

class Forest:
    """
    Holds information about the environment, climate, and collection of trees found in the forest.
    Also might store a list of species found in the environment
    """
    def __init__(self, climate, species=None):
        """
        Input: A list of climate conditions for each month of the year
        Attributes:
            - Climate : [ClimateByMonth]
            - Trees : [Tree]
        """
        # create climate list
        self.climate = self.read_climate_data(climate)

        # initialize list of trees
        self.trees = []

        # create species list
        self.species_list = self.create_species_list(species)


    def read_climate_data(self, climate_filepath):
        """
        Input: Climate CSV file
        Output: A list of 12 ClimateByMonth instances, one for each month.

        TODO I'm separating this out so that in the future I can easily change the
        climate input -- CSV implementation is temporary
        """

        climate_csv = self.read_csv(climate_filepath)
        climate_data = []

        for month in climate_csv:
            month_instance = self.ClimateByMonth(*month)
            climate_data.append(month_instance)

        return climate_data


    def create_species_list(self, species_file):
        """
        Input: Species CSV filepath
        Output: A list of Species class instances, one for each species of tree.
        """
        # convert CSV to list
        species_csv = self.read_csv(species_file)

        # Create a new Species instance for each listed species
        species_list = []
        for species in species_csv:
            species_instance = Species(*species)
            species_list.append(species_instance)

        return species_list
    

    def read_csv(self, file):
        """
        Input: CSV file for either species or climate
        Output: A list of all information in the CSV
        """
        list = []
        with open(file, 'r') as file:
            reader = csv.reader(file)
            next(reader) # skip the header row
            for row in reader:
                # Exclude lines starting with a comment character (e.g., #)
                if not row or row[0].startswith("#"):
                    continue
                list.append(row)
        return list


    def add_tree(self, tree):
        self.trees.append(tree)


    def get_climate(self):
        print("========== GETTING CLIMATE FOR THIS FOREST ==========")
        print("month, tmax (C), tmin (C), rain (cm), solar radiation (kwh/m2), num frost days,\
 soil water (cm/ft), max soil water (cm/ft), soil texture")
        for month in self.climate:
            print(f'{month.month}, {month.tmax}, {month.tmin}, {month.rain}, {month.solar_rad},\
 {month.frost_days}, {month.soil_water}, {month.max_soil_water}, {month.soil_texture}')


    class ClimateByMonth:
        """
        A class that holds information on the climate for one month of the year.
        A ClimateByMonth instance is initialized for each month of the year.
        """
        
        def __init__(self, month:str, tmax:int, tmin:int, r:float, sr:float, fd:int, st:str):
            """
            Attributes:
                - month : str
                - tmax : int
                - tmin : int
                - rain : float
                - solar_rad : float
                - frost_days : int
                - soil_texture : str
                - soil_water : float        Estimated with estimate_soil_water
                - max_soil_water : float
            """
            self.month = month          # January, February, etc.
            self.tmax = tmax            # Average maximum temperature (celsius)
            self.tmin = tmin            # Average minimum temperature (celsius)
            self.rain = r               # Average rainfall (cm)
            self.solar_rad = sr         # Average solar radiation (kwh/m2)
            self.frost_days = fd        # Average number of frost days (int)
            self.soil_texture = st
            
            self.soil_water, self.max_soil_water = self.estimate_soil_water(st)
        

        def estimate_soil_water(self, soil_texture):
            """
            Uses soil texture input to estimate soil water.

            LLM categorizes the type of soil for the area,
            and we approximate its values based on the category
            data from https://ucanr.edu/sites/UrbanHort/files/80243.pdf
            and converted to metric units from in. per ft. of soil
            to cm per ft. of soil

            |-----------------------------------------------|
            | === soil texture ===  | holding capacity (cm) |
            |-----------------------|-----------------------|
            | very coarse sand      | 1.016 - 1.905         |   A
            |-----------------------|-----------------------|
            | coarse sand           |                       |
            | fine sand             | 1.905 - 3.175         |   B
            | loamy sand            |                       |
            |-----------------------|-----------------------|
            | sandy loams           |                       |   C
            | fine sandy loams      | 3.175 - 4.445         |
            |-----------------------|-----------------------|
            | very fine sandy loams |                       |
            | loams                 | 3.81 - 5.842          |   D
            | silt loams            |                       |
            |-----------------------|-----------------------|
            | clay loams            |                       |
            | silt clay loams       | 4.445 - 6.35          |   E
            | sandy clay loams      |                       |
            |-----------------------|-----------------------|
            | sandy clays           |                       |
            | silty clays           | 4.064 - 6.35          |   F
            | clays                 |                       |
            |-----------------------------------------------|
            """
            # Holding capacity A
            if soil_texture == "very_coarse_sand":
                # capacity range
                min = 1.016
                max = 1.905

            # Holding capacity B
            elif soil_texture == "coarse_sand" or \
                soil_texture == "fine_sand" or \
                soil_texture == "loamy_sand":
                # capacity range - lowest in B
                min = 1.905
                max = 3.175
                # TODO refine the categories and apply different
                # sections for each subcategory
                #max = ((max - min) / 3) + min

            # Holding capacity C
            elif soil_texture == "sandy_loams" or \
                soil_texture == "fine_sandy_loams":
                min = 3.175
                max = 4.445
            
            # Holding capacity D
            elif soil_texture == "very_fine_sandy_loams" or \
                soil_texture == "loams" or \
                soil_texture == "silt_loams":
                min = 3.81
                max = 5.842

            # Holding capacity E
            elif soil_texture == "clay_loams" or \
                soil_texture == "silt_clay_loams" or \
                soil_texture == "sandy_clay_loams":
                min = 4.445
                max = 6.35

            # Holding capacity F
            elif soil_texture == "sandy_clays" or \
                soil_texture == "silty_clays" or \
                soil_texture == "clays":
                min = 4.064
                max = 6.35
            else:
                print(f"ERROR Invalid soil texture: {soil_texture}")
                return None
            
            
            soil_water = random.uniform(min,max)
            max_soil_water = max
            return soil_water, max_soil_water


class Species:
    """
    Holds information about a specific species.
    Takes in data collected by parameter estimator

    TODO implement 3-PG calculations here
    """
    def __init__(self, name, name_scientific, 
                 q_leaf_shape, q_canopy_density, q_deciduous_evergreen, q_leaf_color, q_tree_form, 
                 q_tree_roots, q_habitat, q_bark_texture, q_bark_color, 
                 t_min=0, t_opt=0, t_max=0, kf=0, fcax_700=0, kd=0, n_theta=0, c_theta=0, p2=0, p20=0, 
                 acx=0, sla_1=0, sla_0=0, t_sla_mid=0, fn0=0, nfn=0, tc=0, max_age=0, r_age=0, n_age=0, 
                 mf=0, mr=0, ms=0, yfx=0, yf0=0, tyf=0, yr=0, nr_max=0, nr_min=0, m_0=0, wsx1000=0, nm=0, 
                 k=0, aws=0, nws=0, ah=0, nhb=0, nhc=0, ahl=0, nhlb=0, nhlc=0, ak=0, nkb=0, nkh=0, av=0, 
                 nvb=0, nvh=0, nvbh=0, ):
        """
        Attributes are a combination of LLM responses (qualitative) and parameter estimation (quantitative)
        Input from parameter estimation function output
        """
        self.name = name

        # Obtained from LLM:
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

        # Estimated from knowledge base:
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
        pass

    def get_basic_info(self):
        """
        Prints the qualitative data about a tree species. Just for fun, but also for fact checking.
        """
        print(f'========== {self.name} ({self.name_scientific}) ===========')
        print(f'{self.name} are a {self.q_deciduous_evergreen[0]} species, and are commonly found in {", ".join(self.q_habitat)} climates.')
        print(f'FOLIAGE: {self.name} tend to have a {", ".join(self.q_tree_form)} form, with {", ".join(self.q_leaf_color)}, {", ".join(self.q_leaf_shape)}-type leaves.')
        print(f'WOOD: The bark of {self.name} have a {" or ".join(self.q_bark_texture)} texture and tend to be {" and ".join(self.q_bark_color)} in color.\n')


class Tree(Species):
    """
    Holds information about each individual tree in the forest.
    Inherits information about its species
    Calculates unique dimensions on initialization
    Initialization occurs when the (x,y) coordinates are generated
    """
    def __init__(self, species, x, y):
        pass


"""
=====================================================================
                                FUNCTIONS
=====================================================================
"""

def create_forest(climate_fp, species_fp):
    # 1. Initialize forest
    # read in the climate data
    # initialize the forest based on climate data
    forest = Forest(climate_fp, species_fp)
    forest.get_climate()
    for species in forest.species_list:
        species.get_basic_info()

    # 2. Compute data for each species

    # 3. Create indivisual trees from species data

    # 4. Repeat for spawned/killed trees

    # 5. Write to Blender
    pass

if __name__ == '__main__':
    # example usage here
    create_forest("test_data/prineville_oregon_climate.csv", "test_data/param_est_output.csv")