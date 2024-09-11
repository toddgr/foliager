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
import math
from gauss import Gaussian

E = 2.718
PI = 3.1415

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
    def __init__(self, climate, species=None, num_trees=None):
        """
        Input: A list of climate conditions for each month of the year
        Attributes:
            - Climate : [ClimateByMonth]
            - Trees : [Tree]
        """
        # create climate list
        self.climate_list = self.read_climate_data(climate)

        # initialize list of trees
        self.trees_list = []
        self.num_trees = num_trees

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
        self.trees_list.append(tree)


    def get_climate(self):
        print("========== GETTING CLIMATE FOR THIS FOREST ==========")
        print("month, tmax (C), tmin (C), rain (cm), solar radiation (kwh/m2), num frost days,\
 soil water (cm/ft), max soil water (cm/ft), soil texture")
        for month in self.climate_list:
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
                 leaf_shape, canopy_density, deciduous_evergreen, leaf_color, tree_form, 
                 tree_roots, habitat, bark_texture, bark_color, 
                 t_min=0, t_opt=0, t_max=0, kf=0, fcax_700=0, kd=0, n_theta=0, c_theta=0, p2=0, p20=0, 
                 acx=0, sla_1=0, sla_0=0, t_sla_mid=0, fn0=0, nfn=0, tc=0, max_age=0, r_age=0, n_age=0, 
                 mf=0, mr=0, ms=0, yfx=0, yf0=0, tyf=0, yr=0, nr_max=0, nr_min=0, m_0=0, wsx1000=0, nm=0, 
                 k=0, aws=0, nws=0, ah=0, nhb=0, nhc=0, ahl=0, nhlb=0, nhlc=0, ak=0, nkb=0, nkh=0, av=0, 
                 nvb=0, nvh=0, nvbh=0, ):
        """
        Attributes are a combination of LLM responses (qualitative) and parameter estimation (quantitative)
        Input from parameter estimation function output, quantitative values default to 0 if not found
        """
        self.name:str = name
        self.name_scientific:str = name_scientific

        # Obtained from LLM (all are lists of strings):
        self.leaf_shape = leaf_shape.split('/')
        self.leaf_color = leaf_color.split('/')

        self.tree_form = tree_form.split('/')
        self.tree_roots = tree_roots.split('/')

        self.canopy_density = canopy_density.split('/')
        self.q_deciduous_evergreen = deciduous_evergreen.split('/')
        self.habitat = habitat.split('/')

        self.bark_texture = bark_texture.split('/')
        self.bark_color = bark_color.split('/')

        # Estimated from knowledge base:
        self.t_min = float(t_min)
        self.t_opt = float(t_opt)
        self.t_max = float(t_max)
        self.kf = float(kf)
        self.fcax_700 = float(fcax_700) #  assimilation enhancement factor at 700 ppm
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
        
        # Data calculated from 3-PG:
        # species height, species dbh, species live crown length, species crown diameter
        self.height = 0
        self.dbh = 0
        self.lcl = 0
        self.c_diam = 0


    def get_basic_info(self):
        """
        Prints the qualitative data about a tree species. Just for fun, but also for fact checking.
        """
        print(f'\n========== {self.name} ({self.name_scientific}) ===========')
        print(f'{self.name} are a {self.q_deciduous_evergreen[0]} species, and are commonly found in {", ".join(self.habitat)} climates.')
        print(f'FOLIAGE: {self.name} tend to have a {", ".join(self.tree_form)} form, with {", ".join(self.leaf_color)}, {", ".join(self.leaf_shape)}-type leaves.')
        print(f'WOOD: The bark of {self.name} have a {" or ".join(self.bark_texture)} texture and tend to be {" and ".join(self.bark_color)} in color.\n')


class Tree(Species):
    """
    Holds information about each individual tree in the forest.
    Inherits information about its species
    Calculates unique dimensions on initialization
    Initialization occurs when the (x,y) coordinates are generated
    """
    def __init__(self, species, x, y):
        """
        Attributes:
            Inherited
            - name
            - bark_texture
            - bark_color
            - leaf_shape
            - tree_form
            Calculated
            - position (x, y) -> from coordinate generator
            - height -> from species, with randomization
            - dbh
            - lcl
            - c_diam
        """
        self.name = species.name
        self.bark_texture = species.bark_texture
        self.bark_color = species.bark_color
        self.leaf_shape = species.leaf_shape
        self.tree_form = species.tree_form

        self.position = (x,y)
        self.height = self.generate_from(species.height)
        self.dbh = self.generate_from(species.dbh)
        self.lcl = self.generate_from(species.lcl)
        self.c_diam = self.generate_from(species.c_diam)

        self.key = self.create_tree_key() # e.g. Ponderosa243123

        pass

    def generate_from(self, dimension):
        """
        Input: Some dimension from the species
        Output: A slightly randomized variation of that dimension for the tree
                using gaussian randomization
        """
        average = dimension
        stddev = 1 # TODO make this var more accurate

        new_dimension = Gaussian(average, stddev)
        return abs(new_dimension) # dimension can't be negative
    

    def create_tree_key(self):
        """
        Input: Unique position of the tree
        Output: A string that will uniquely represent the tree.
                First word of the name + x + y
                i.e. Ponderosa184339
        """

        name = self.name.split()[0] # First word of the species name
        x = str(int(self.position[0] * 1000)) # ex. 0.183444 -> '183'
        y = str(int(self.position[1] * 1000)) # ex. 0.234950 -> '234'

        return name + x + y


    def get_tree_info(self):
        print(f'========== {self.key} ==========')
        print(f'position: {self.position}\nheight: {self.height}\ndbh: {self.dbh}')
        print(f'lcl: {self.lcl}\nc_diam: {self.c_diam}\n')

"""
=====================================================================
                                FUNCTIONS
=====================================================================
"""

def threepg(forest:Forest, t:int):
    """
    Input: Forest (climate, species), time interval (in months)
    Output: Updated forest, with specific dimensions for each species
            at the time interval?
    """
    # Initial biomasses -- all are in tonnes of dry mass per hectare, or tDM/ha
    # TODO need to figure out what these values should be, and if they should be 
    #       different for each species
    init_foliage_biomass = 1. #7.
    init_root_biomass = 1. #9.
    init_stem_biomass = 1. #20.

    # for each of the species in the list:
    for species in forest.species_list:
        # initialize biomass
        last_foliage_biomass = init_foliage_biomass
        last_stem_biomass = init_stem_biomass
        last_root_biomass = init_root_biomass

        init_dbh = 0. #9 initial dbh-- was 18 TODO determine init_dbh

        co2 = 350 # Atmospheric CO2 (ppm) TODO Implement estimated CO2 function taken from NASA data: https://climate.nasa.gov/vital-signs/carbon-dioxide/?intent=121
        mean_vpd = 1. # mean daytime VPD (kPa) TODO Implement estimated VPD function and put this in monthly climate data

        # general for GPP
        fertility_rating = 1 # fertility rating, ranges from 0 to 1
        conversion_ratio = 0.47 # for making GPP into NPP

        start_age = 5 # this is the stand's age in years at t = 0
        start_month = 5 # this is the number of the month in which the simulation is beginning
        start_year = 2024 # this is the year the simulation was started. TODO Used for prints only?
        
        num_trees_died = 0 # number of trees that died last month. TODO Use this for killing trees

        # for each month in the time interval:
        for month_t in range(t+1):
            # get the current month, mean temp for the month
            climate = forest.climate_list
            current_month = ((start_month + month_t) % 12)-1 # jan - dec
            if current_month == 0:
                current_month = 11

            mean_monthly_temp = (climate[current_month].tmax + climate[current_month].tmin)/2.

            # === calculate mods (can be its own independent function i think) ===
            # temperature mod (ft)
            if (mean_monthly_temp > species.t_max) or (mean_monthly_temp < species.t_min):
                # outside of growth range -> 0
                ft = 0. # TODO temp mod
            else:
                # inside of growth range
                base = (mean_monthly_temp - species.t_min / (species.t_opt - species.t_min) * (species.t_max - mean_monthly_temp)/(species.t_max - species.t_opt))
                exp = (species.t_max - species.t_opt)/(species.t_opt - species.t_min)
                ft = pow(base, exp) #TODO temp mod
            
            # frost mod
            frost_days = climate[current_month].frost_days # aka df
            ff = 1. - species.kf * (frost_days/30.) #TODO frost mod

            # nutrition mod
            fn = 1. - (1. - species.fn0) * pow((1. - fertility_rating), species.nfn) # TODO nutrition mod

            # CO2 mod
            fcax = species.fcax_700/(2. - species.fcax_700) # the species specific repsonses to changes in atmospheric co2
            fc = fcax * co2/(350. * (fcax - 1.) + co2) # TODO c02 mod - is '350' need to be changed to co2? Research this formula

            # physical mod - derived from fd, ftheta
            # vapor pressure deficit (VPD) mod
            fd = pow(E, (-species.kd * mean_vpd)) # TODO VPD mod

            # soil water mod
            base1 = ((1. - climate[current_month].soil_water)/climate[current_month].max_soil_water)/species.c_theta
            ftheta = 1./(1. + pow(base1, species.n_theta))

            physmod = fd * ftheta # TODO verify we don't need fa

            # specific leaf area (SLA)
            exp1 = pow(((start_age * 12.) + month_t)/species.t_sla_mid, 2.)
            sla = species.sla_1 + (species.sla_0 - species.sla_1) * pow(E, (-1 * math.log(2.) * exp1))

            # leaf area index (m^2 / m^2)
            leaf_area_index = 0.1 * sla * last_foliage_biomass

            # ground area coverage (GAC) by canopy
            if start_age + month_t / 12 < species.tc:
                ground_area_coverage = (start_age + month_t / 12) / species.tc
            else:
                ground_area_coverage = 1. # TODO verify this makes sense

            # light absorption --> absorption photosynthetically active radiation (PAR)
            # Often called o/pa
            e_exp = (-species.k * leaf_area_index)/ground_area_coverage
            par = (1 - pow(E, e_exp)) * 2.3 * ground_area_coverage * climate[current_month].solar_rad

            # computing GPP and NPP
            gpp = ft * ff * fn * fc * physmod * species.acx * par
            npp = gpp * conversion_ratio

            # partitioning ratios
            # computing m --> linear function of FR (fertility rating)
            m = species.m_0 + ((1. - species.m_0) * fertility_rating)

            # root partitioning ratio
            root_partition_ratio = (species.nr_min * species.nr_max) / (species.nr_min + ((species.nr_max - species.nr_min) * m * physmod))

            # compute np and ap, which are used to calculate pfs TODO what are these
            np = (math.log(species.p20/species.p2))/math.log(10.) # equation A29
            ap = species.p2/(pow(2., np)) # equation A29

            b = 1 # TODO what is b?
            pfs = ap * pow(b, np)

            # getting remaining partitioning ratios
            nf = (pfs * (1. - root_partition_ratio))/(1. + pfs) # TODO foliage partition
            ns = (1. - root_partition_ratio)/(1. + pfs) # TODO soil partition

            # computer litterfall
            current_age = start_age + t/12 # TODO start_age is in years? This feels wrong
            # according to 3-PG manual, page 33:
                # For deciduous species, the litterfall rates yf0 and yfx may be considered 
                # to be 0 because all of the foliage is lost at the end of the growing season anyway.
            if species.q_deciduous_evergreen == ['deciduous'] and (species.yf0 == 0 or species.yfx == 0):
                litterfall_rate = 0  # otherwise we get a divide by zero
            else: 
                lf_exp = -(current_age/species.tyf) * math.log(1.0 + species.yfx/species.yf0)
                litterfall_rate = (species.yfx * species.yf0)/(species.yf0 + (species.yfx - species.yf0) * pow(E, lf_exp))

            # compute biomass
            # setting current = to last month's
            curr_foliage_biomass = last_foliage_biomass
            curr_stem_biomass = last_stem_biomass
            curr_root_biomass = last_root_biomass
            
            # increment the current using last month's values
            curr_foliage_biomass += (nf * npp) - (litterfall_rate * last_foliage_biomass) - (species.mf * (last_foliage_biomass / forest.num_trees) * num_trees_died)
            curr_root_biomass += (root_partition_ratio * npp) - (species.yr * last_root_biomass) - (species.mr * (last_root_biomass / forest.num_trees) * num_trees_died)
            curr_stem_biomass += (ns * npp) - (species.ms * (last_stem_biomass / forest.num_trees) * num_trees_died)

            # making the current into last month's for the next month
            if curr_foliage_biomass > 0.:
                last_foliage_biomass = curr_foliage_biomass
            if curr_stem_biomass > 0.:
                last_stem_biomass = curr_stem_biomass
            if curr_root_biomass > 0.:
                last_root_biomass = curr_root_biomass

            # resetting TODO should we reset this here?
            num_trees_died = 0

            # ======================================================================

            # check if we need to thin/kill some trees
            # mortality
            # max individual tree stem mass (wsx)
            max_ind_tree_stem_mass_wsx = species.wsx1000 * pow((1000.0/forest.num_trees), species.nm)
            while last_stem_biomass / num_trees > max_ind_tree_stem_mass_wsx and num_trees > 0:
                # need to thin
                num_trees -= 1  # decreasing n
                num_trees_died += 1 # increasing delta_n counter
                max_ind_tree_stem_mass_wsx = species.wsx1000 * pow((1000.0/num_trees), species.nm) # recalculating wsx

            # === compute dimensions based on parameters ===
            # TODO add C index here
            # TODO implement relative height

            # calculating b from mean individual stem mass (inversion of A65 of user manual)
            ind_stem_mass_iws = last_stem_biomass / num_trees # individual stem mass
            b = pow(ind_stem_mass_iws/species.aws, (1.0/species.nws)) *100

            # bias correction to adjust b TODO implement later?

            # mean tree height TODO what is the difference between species formula and individual tree formula?
            mean_tree_height = 1.3 + species.ah * pow(E, (-species.nhb/b)) + species.nhc * b # for single tree species

            # live crown length TODO same thing
            live_crown_length = 1.3 + species.ahl * pow(E, (-species.nhlb/b)) + species.nhlc * b

            # crown diameter
            crown_diameter = species.ak * pow(b, species.nkb) * pow(mean_tree_height, species.nkh)

            # basal area
            ba = (PI * b * b)/40000

            # stand volume TODO not used
            stand_volume = species.av * pow(b, species.nvb) * pow(mean_tree_height, species.nvh) * pow(b * b * mean_tree_height, species.nvbh) * forest.num_trees
    
            # diameter at breast height
            dbh = math.sqrt((4 * ba) / PI) # trunk of the standing trees

            # Assign to species
            species.height = mean_tree_height
            species.lcl = live_crown_length
            species.c_diam = crown_diameter
            species.dbh = dbh
    pass

def create_forest(climate_fp, species_fp, num_trees = 100, t = 60):
    # 1. Initialize forest
    # read in the climate data
    # initialize the forest based on climate data
    forest = Forest(climate_fp, species_fp, num_trees)

    # 2. Compute 3-PG data for each species

    # 3. Create individual trees from species data

    # 4. Repeat for spawned/killed trees

    # 5. Write to Blender
    
    return forest

if __name__ == '__main__':
    # example usage here
    forest = create_forest("test_data/prineville_oregon_climate.csv", "test_data/param_est_output.csv", num_trees=1200)
    
    forest.get_climate()
    
    for species in forest.species_list:
        species.get_basic_info()

    tree = Tree(forest.species_list[0], 0.234323432, 0.123219347093)
    tree.get_tree_info()