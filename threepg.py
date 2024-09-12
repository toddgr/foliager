"""
File: 3pg.py
Author: Grace Todd
Date: September 10, 2024
Description: Uses 3-PG to calculate various parameters of a tree, which will be used to generate
             each tree in the simulation at every time interval.
             
             Based on real, scientific data, and uses C++ skeleton framework provided by Allison
             Thompson in her thesis here: https://ir.library.oregonstate.edu/concern/honors_college_theses/x920g532g.
"""

import math # for log
from threepg_species_data import parse_species_data
from parse_tree_input import csv_file_to_list
from plot_trees_random import init_trees_dont_write_yet
import csv
import random
import itertools


class TreeViz:
    """
        For visualizing the trees, originally in C++ code from Allison Thompson
    """
    def __init__(self, x, z, dbh_dev, height_dev, draw) -> None:
        self.position = (x, z)          # X and Z coordinates of the spawn point (?) of the tree
        self.dbh_dev = dbh_dev          # Diameter of breast height
        self.height_dev = height_dev    # height of the tree
        self.draw = draw                # Bool -- either draw or don't draw the tree


class Tree:
    """
        For holding the data for each individual tree in the simulation.
    """
    def __init__(self, t:int, name:str, bark_texture:list, bark_color:list, height:float, dbh:float, lcl:float, c_diam:float, 
                 x:float=None, z:float=None, is_dead:bool=None, masting_cycle:int=None, age:int=None, stage:str=None):
        self.t = t
        self.name = name
        self.bark_texture = bark_texture
        self.bark_color = bark_color
        self.position = (x,z)
        self.height = height
        self.dbh = dbh
        self.lcl = lcl
        self.c_diam = c_diam
        self.is_dead = is_dead
        self.masting_cycle = masting_cycle
        self.age = age
        self.stage = stage


"""
    CLIMATE DATA
"""
class Month:
    """
        Holds important information for visualization based on data from the site about the current month.
        Derived and estimated from LLM.
    """
    def __init__(self, site_tmax, site_tmin, site_rain, site_solar_rad, site_frost_days, site_soil_texture, site_soil_water=0, site_max_soil_water=0):
        self.tmax = site_tmax   # Average maximum temperature for the month (C)
        self.tmin = site_tmin   # Average minimum temperature for the month (C)
        self.rain = site_rain   # Average rainfall for the month (cm)
        self.solar_rad = site_solar_rad # Average solar radiation for the month (kwh/m2)
        self.frost_days = site_frost_days   # Average number of frost days for the month (int)
        self.soil_texture = site_soil_texture # Average soil texture of the site -- used to estimate:
        self.soil_water = site_soil_water           # Average amount of soil water (cm water per ft of soil)
        self.max_soil_water = site_max_soil_water   # Maximum possible soil water (cm of water per ft of soil)

# CO2 
# fcax_700 = douglasfir.fcax_700 # This one is the "assimilation enhancement factor at 700 ppm" "parameter[s] define the species specific repsonses to changes in atmospheric co2"
co2 = 350 # Atmospheric CO2 (ppm) TODO Implement estimated CO2 function taken from NASA data: https://climate.nasa.gov/vital-signs/carbon-dioxide/?intent=121

# VPD 
mean_vpd = 1. # mean daytime VPD (kPa) TODO Implement estimated VPD function and put this in monthly climate data
# kd defines the stomatal response to VPD

"""
    ==================== STAND DATA ========================
    This data is about the stand in question. . 
"""

# Initial biomasses -- all are in tonnes of dry mass per hectare, or tDM/ha
init_foliage_biomass = 1. #7.
init_root_biomass = 1. #9.
init_stem_biomass = 1. #20.

init_dbh = 0. #9 # initial dbh-- was 18
#init_sw = 0. #200   # initial available soil water

# general for GPP
fertility_rating = 1 # fertility rating, ranges from 0 to 1

start_age = 5 # this is the stand's age in years at t = 0
start_month = 5 # this is the number of the month in which the simulation is beginning
start_year = 2024 # this is the year the simulation was started. Used for prints only?

#physmod_method = 0 # this denotes the method used to calculate physmod. 0 = combo 1= limiting
#agemod_method = 0 # 0 = agemod not used, 1 = agemod used

conversion_ratio = 0.47 # conversion ratio for making GPP into NPP

"""
    ==================== 3PG OUTPUTS ========================
num_trees = trees per square hectare
gpp = gross primary production
npp = net primary production
wf = foliage biomass (Mg/ha which is megagramme/hectare, a megagramme is a tonne)
wr = root biomass (Mg/ha)
ws = stem biomass (Mg/ha)
par = absorption of photosynthetically active radiation
mean_stem_mass comes from the mortality calculations? We think
live_crown_length = length of live portion of tree foliage
crown_base_height = how far off ground does the live crown start
b =  mean diameter at breast height, aks B or DBH (cm)
h = mean total tree height, aka H (m)
hl = live crown length (m)
k = crown diameter (m)
ba = basal area (m^2)
vs = stand volume (m^3/ha)
gac = proportion of ground area covered by the canopy
"""


def approximate_soil_data(soil_texture):
    """ NLP categorizes the type of soil for the area,
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


def read_climate_data(file_path):
    """
        Reads in a CSV file that contains climate data for each month of the year
        Derived from and approximated by LLM
    """
    month_data = []  # Assuming monthdata is a list of objects with attributes site_tmax, site_tmin, etc.
    init_month_data = []  # Assuming initmonthdata is also a list of objects with similar attributes

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        i = 0
        for row in reader:
            soil_texture = row['soil_texture']
            soil_water, max_soil_water = approximate_soil_data(soil_texture)
            #print(f"soil_water: {soil_water}, max_soil_water: {max_soil_water}")

            month_data.append(Month(
                site_tmax = float(row['tmax']),
                site_tmin = float(row['tmin']),
                site_rain = float(row['rain']),
                site_solar_rad = float(row['solar_rad']),
                site_frost_days = float(row['frost_days']),
                site_soil_texture = soil_texture,
                site_soil_water = soil_water,
                site_max_soil_water=max_soil_water
            ))

            init_month_data.append(Month(
                site_tmax=month_data[i].tmax,
                site_tmin=month_data[i].tmin,
                site_rain=month_data[i].rain,
                site_solar_rad=month_data[i].solar_rad,
                site_frost_days=month_data[i].frost_days,
                site_soil_texture=month_data[i].soil_texture,
                site_soil_water=soil_water,
                site_max_soil_water=max_soil_water
            ))
            i = i + 1

    return month_data, init_month_data


def parse_env_data(file_path):
    """ Parses through the environment data for the forest
        (inlcudes both climate data and stand data) to be 
        used in 3-PG 
        TODO Not being used at the moment
    """
    # Parse the CSV line into a list
    env_list = csv_file_to_list(file_path)
    # Put those values into an Environment class
    env_data_list = []

    for month_data in env_list:
        env_instance = Month(*month_data)
        env_data_list.append(env_instance)

    return env_data_list

"""
    ================= COMPUTE THE OUTPUTS ====================
    Need to break this up a little bit, we'll see if that's possible.
    Assigns and calculates values for all of the globals defined above. 
    Now that I think of it... breaking this up might help to optimize the process. Maybe.
"""
def compute(environment_data_filename, speciesdata_filename, t, num_trees=1200):
    """
        Takes in climate data, species data, time in months since beginning of simulation
        Computes the outputs for the 3-PG algorithm
    """
    E = 2.718
    PI = 3.1415

    #num_trees = 1200 # number of trees per square hectare
    speciesdata_list = parse_species_data(speciesdata_filename)
    #environment = parse_env_data(environment_data_filename)
    height_dbh_list = []
    tree_list = []
    for species in speciesdata_list:
        #print(f"SPECIES: {species.name}, max soil water = {species.max_soil_water}, soil_water = {species.soil_water}")
        month_data, _ = read_climate_data(environment_data_filename)
        # values of biomass pools that will be used throughout the incremental calculations
        last_foliage_biomass = init_foliage_biomass
        last_stem_biomass = init_stem_biomass
        last_root_biomass = init_root_biomass

        num_trees_died = 0 # number of trees that died last month TODO mess with this

        for month_t in range(t+1): # t that will be used as an iterator throughout the incremental calculations
            current_month = ((start_month + month_t) % 12)-1
            if current_month == 0:
                current_month = 11

            # compute the PAR/aC mods
            # temperature mod
            #ft = 1.
            mean_monthly_temp = (month_data[current_month].tmax + month_data[current_month].tmin)/2. # getting mean monthly temp from site data
            if (mean_monthly_temp > species.t_max) or (mean_monthly_temp < species.t_min):
                # outside of growth range -> 0
                ft = 0.
            else:
                # inside of growth range
                base = (mean_monthly_temp - species.t_min / (species.t_opt - species.t_min) * (species.t_max - mean_monthly_temp)/(species.t_max - species.t_opt))
                exp = (species.t_max - species.t_opt)/(species.t_opt - species.t_min)
                ft = pow(base, exp)

            # frost mod
            df = month_data[current_month].frost_days
            ff = 1. - species.kf * (df/30.) 

            # nutrition mod
            fn = 1. - (1. - species.fn0) * pow((1. - fertility_rating), species.nfn)

            # C02 mod
            fc = 1
            fcax = species.fcax_700/(2. - species.fcax_700) # we're not exactly sure that this does
            fc = fcax * co2/(350. * (fcax - 1.) + co2) # TODO fix this later

            # phys mod stuff --> made from a combo of fd, ftheta, and age mod
            # vapor pressure deficit (VPD) mod
            fd = pow(E, (-species.kd * mean_vpd))

            # soil water mod
            base1 = ((1. - month_data[current_month].soil_water)/month_data[current_month].max_soil_water)/species.c_theta
            ftheta = 1./(1. + pow(base1, species.n_theta))

            # age mod --> used if denoted in glui
            # TODO maybe just not use this?
            fa = 1.
            # if agemod_method:
            #     age_base = ((age0 + (inc_t / 12.))/species.max_age)/species.r_age
            #     fa = 1. / (1. + pow(age_base, species.n_age))
            
            # calculating phys mod
            # physmod = 1.
            # if physmod_method:
            #     # limiting physmod, uses only most limiting of vpd and soil water mods
            #     lim = fd if fd <= ftheta else ftheta
            #     physmod = fa * lim
            # else:
            #     # combo physmod, both vpd and soil water mods influence physmods
            physmod = fa * fd * ftheta
            
            # SLA -- specific leaf area
            exp1 = pow(((start_age * 12.) + month_t)/species.t_sla_mid, 2.)
            sla = species.sla_1 + (species.sla_0 - species.sla_1) * pow(E, (-1 * math.log(2.) * exp1))

            # leaf area index (m^2 / m^2)
            leaf_area_index = 0.1 * sla * last_foliage_biomass

            # GAC --> percentage of ground area covered by canopy
            if start_age + month_t / 12 < species.tc:
                ground_area_coverage = (start_age + month_t / 12) / species.tc
            else:
                ground_area_coverage = 1.
            #print(f"GAC: {gac}")
            
            # light absorption --> absorption photosynthetically active radiation (PAR)
            # Often called o/pa
            #print(f"e_exp = (-{species.k} *  {l} / {gac})")
            e_exp = (-species.k * leaf_area_index)/ground_area_coverage
            par = (1. - pow(E, e_exp)) * 2.3 * ground_area_coverage * month_data[current_month].solar_rad # the delta t is excluded because it will always be 1
        
            # Computing GPP and NPP
            gpp = ft * ff * fn * fc * physmod * species.acx * par
            npp = gpp * conversion_ratio

            # Partitioning ratios
            # computing m --> linear function of FR (fertility rating)
            m = species.m_0 + ((1. - species.m_0) * fertility_rating)

            # computing the root partitioning ratio
            root_partition_ratio = (species.nr_min * species.nr_max) / (species.nr_min + ((species.nr_max - species.nr_min) * m * physmod))

            # computing np and ap, which are used to calculate pfs
            np = (math.log(species.p20/species.p2))/math.log(10.) # equation A29
            ap = species.p2/(pow(2., np)) # equation A29

            # computing pfs
            b = 1
            pfs = ap * pow(b, np) # Ratio of soil biomass : foliage biomass

            # getting remaining partitioning ratios
            nf = (pfs * (1. - root_partition_ratio))/(1. + pfs)
            ns = (1. - root_partition_ratio)/(1. + pfs)

            # mortality
            # max individual tree stem mass (wsx)
            max_ind_tree_stem_mass_wsx = species.wsx1000 * pow((1000.0/num_trees), species.nm)

            # check if we need to thin
            while last_stem_biomass / num_trees > max_ind_tree_stem_mass_wsx and num_trees > 0:
                # need to thin
                num_trees -= 1  # decreasing n
                num_trees_died += 1 # increasing delta_n counter
                max_ind_tree_stem_mass_wsx = species.wsx1000 * pow((1000.0/num_trees), species.nm) # recalculating wsx

            # litterfall
            current_age = start_age + t/12
            # according to 3-PG manual, page 33:
                # For deciduous species, the litterfall rates yf0 and yfx may be considered 
                # to be 0 because all of the foliage is lost at the end of the growing season anyway.
            if species.q_deciduous_evergreen == ['deciduous'] and (species.yf0 == 0 or species.yfx == 0):
                litterfall_rate = 0  # otherwise we get a divide by zero
            else: 
                lf_exp = -(current_age/species.tyf) * math.log(1.0 + species.yfx/species.yf0)
                litterfall_rate = (species.yfx * species.yf0)/(species.yf0 + (species.yfx - species.yf0) * pow(E, lf_exp))

            # Computing biomass
            # using init_wx and just plain num_trees here because this is designed to be 
            # calculated from any point in the simulation.

            # doing this on a monthly time step

            # setting current = to last month's
            curr_foliage_biomass = last_foliage_biomass
            curr_stem_biomass = last_stem_biomass
            curr_root_biomass = last_root_biomass

            # increment the current using last month's values
            curr_foliage_biomass += (nf * npp) - (litterfall_rate * last_foliage_biomass) - (species.mf * (last_foliage_biomass / num_trees) * num_trees_died)
            curr_root_biomass += (root_partition_ratio * npp) - (species.yr * last_root_biomass) - (species.mr * (last_root_biomass / num_trees) * num_trees_died)
            curr_stem_biomass += (ns * npp) - (species.ms * (last_stem_biomass / num_trees) * num_trees_died)

            # making the current into last month's for the next month
            if curr_foliage_biomass > 0.:
                last_foliage_biomass = curr_foliage_biomass
            if curr_stem_biomass > 0.:
                last_stem_biomass = curr_stem_biomass
            if curr_root_biomass > 0.:
                last_root_biomass = curr_root_biomass

            num_trees_died = 0 # resetting 

            # Computing miscellaneous parameters
            # these are all just for printing out, not viz...
            """NOTE: for all the below stand level variables, the C parameter has been left out. 
                C is a competition index and is only applicable to mixed species stands, which this
                implementation does not cover. However, if you were to adapt this implementation to 
                account for mixed species stands, it would be easy to add in the C parameter here
                in the future, as described in section 11.11 of Forrester's User Manual. rh (relative
                height) has also been left out for the same reason.
                TODO: Add in the C parameter here
                TODO implement relative height
            """

            # These are all empirical parameters and are species-specific. They are only used here.
            # all values are from Forrester et al in press from Forrester's excel sheet unless otherwise noted.
            # aws and ans are from forrester et al

            aws = species.aws
            nws = species.nws

            ah = species.ah
            nhb = species.nhb
            nhc = species.nhc

            ahl = species.ahl
            nhlb = species.nhlb
            nhlc = species.nhlc

            ak = species.ak
            nkb = species.nkb
            nkh = species.nkh

            av = species.av
            nvb = species.nvb
            nvh = species.nvh
            nvbh = species.nvbh

            # calculating b from mean individual stem mass (inversion of A65 of user manual)
            ind_stem_mass_iws = last_stem_biomass / num_trees # individual stem mass
            b = pow(ind_stem_mass_iws/aws, (1.0/nws)) *100

            # bias correction to adjust b
            # TODO implement later?

            # mean tree height
            mean_tree_height = 1.3 + ah * pow(E, (-nhb/b)) + nhc * b # for single tree species
            #h = ah * pow(b, nhb) # for data from individual tree data, not used

            # live crown length
            live_crown_length = 1.3 + ahl * pow(E, (-nhlb/b)) + nhlc * b # for single tree species
            #hl = ahl * pow(b, nhlb) * pow(hl, nhll) # for data from individual tree data, not used

            # crown diameter
            crown_diameter = ak * pow(b, nkb) * pow(mean_tree_height, nkh)

            # basal area
            ba = (PI * b * b)/40000

            # stand volume
            stand_volume = av * pow(b, nvb) * pow(mean_tree_height, nvh) * pow(b * b * mean_tree_height, nvbh) * num_trees

            total_height = mean_tree_height # mean tree height
            dbh = math.sqrt((4 * ba) / PI) # trunk of the standing trees
            # TODO: approximate masting cycle here
            # TODO: create an individual tree class (maybe from treeviz?)
            height_dbh_list.append([month_t, species.name, species.q_bark_texture, species.q_bark_color, total_height, dbh, live_crown_length, crown_diameter])
            tree_list.append(Tree(month_t, species.name, species.q_bark_texture, species.q_bark_color, height=total_height, dbh=dbh, lcl=live_crown_length, c_diam=crown_diameter))

        # some test prints
        print(f"\n=== t={t} for {species.name} ===")
        print(f"Live crown length: {live_crown_length}\ncrown diameter: {crown_diameter}\nbasal area: {ba}\nstand volume: {stand_volume}")

    return height_dbh_list, tree_list
            

def create_tree_key(tree_count=-1, tree_key=None, spawn_count=0):
    """ Creates a unique dictionary key for tree children of original trees """
    # Generate all combinations of three letters from 'a' to 'z'
    three_letter_strings = [''.join(letters) for letters in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=3)]

    if tree_key is None: # original tree
        return three_letter_strings[tree_count]
    else:
        return tree_key + str(spawn_count)


def randomize_tree_factors(species):
    """ 
        Slightly randomizes various dimensions of trees to add visual
        differentiation
        TODO implement Gaussian randomization and tree class 
    """
    i = 0
    # Randomized offsets -- different for each tree
    #print(f"=====SPECIES:==== {species} \n ==== ")
    factor_height = float(species.height) / 4
    random_height_offset = random.uniform(-factor_height, factor_height)

    factor_dbh = float(species.dbh) / 4
    random_dbh_offset = random.uniform(-factor_dbh, factor_dbh)
    
    factor_lcl = float(species.lcl) / 4
    random_lcl_offset = random.uniform(-factor_lcl, factor_lcl)
    
    factor_c_diam = float(species.c_diam) / 4
    random_c_diam_offset = random.uniform(-factor_c_diam, factor_c_diam)
    i += 1

    # TODO return something more dynamic
    return [random_height_offset, random_dbh_offset, random_lcl_offset, random_c_diam_offset]
    
# =============================================================================================
# End Debug

def create_tree_list(tree_coordinates, tree_species, t):
    """ Creates the list/dict of tree information for every single tree in the forest. 
        Taking it out of the 3PG function for better readability and also to isolate the 
        data structure so I can mess with it a little bit.

        This is so that we can access multiple instances of the same tree at different time values, and 
        also to make it easier to spawn/kill off trees in an organized way.

        Then, once ALL of the data has been written for all the trees at all the times, then we can write
        it in CSV form, where each tree for each line is written in chronological order.

        TODO instead of a big array like this as the value, have the tree object
    """
    tree_dict = {'# tree_key':[['t', 'name', 'bark_texture', 'bark_color', 'x', 'z', 'height', 'dbh', 'lcl', 'c_diameter', 'is_dead', 'masting_cycle', 'age', 'stage']]}
    key_counter = -1
    is_dead = False
    # TODO: create a parameter estimation for this
    masting_cycle = 5 * 12 # in years -- so 5 years

    # random_factors = randomize_tree_factors(tree_species) # [height, dbh, lcl, c_diam]

    for tree in tree_coordinates[1:]: # for each tree in the forest
        key_counter += 1
        tree_key = create_tree_key(key_counter)
        tree_dict[tree_key] = []
       
        for sp_tree in tree_species:
            #print(f"sp_tree: {sp_tree}. tree_species:{tree_species}")
            create_species_information(sp_tree, tree_dict, masting_cycle, tree, tree_key)

    return tree_dict


def create_species_information(species, tree_dict, masting_cycle, tree, tree_key, age=0):
    """
        Finds the specific tree's species information and assigns it to the tree for each time
        interval that it is not dead
    """
    name = tree[0]
    inc_t=60

    random_factors = randomize_tree_factors(species) # [height, dbh, lcl, c_diam]

    #t, species.name, species.bark_texture, species.bark_color, x, z, total_height, dbh, live_crown_length, crown_diameter, is_dead, masting_cycle
    species_name = species.name
    if name == species_name:
        add_to_tree_dict(species, tree_dict, tree_key, random_factors, tree, name, masting_cycle, age, inc_t)
        inc_t += 1
        age += 1


def add_to_tree_dict(species, tree_dict, tree_key, random_factors, tree, name, masting_cycle, age, inc_t, is_dead=False):
    found = False
    stage = determine_tree_stage(age)
    bark_texture = species.bark_texture
    bark_color = species.bark_color

    if inc_t == species.t: # if it's the correct t value we're looking for
        # if inc_t > 0 and not tree_dict[tree_key][inc_t-1][9]:# If the previous t value of the tree is dead
        #     return #TODO fix

        # assign slightly randomized values to the height and dbh
        new_height = float(species.height) + random_factors[0]
        new_dbh = float(species.dbh) + random_factors[1]
        new_lcl = float(species.lcl) + random_factors[2]
        new_c_diam = float(species.c_diam) + random_factors[3]
        
        # append it to the entry
        tree_entry = [inc_t, name, bark_texture, bark_color, tree[1], tree[2], new_height, new_dbh, new_lcl, new_c_diam, is_dead, masting_cycle, age, stage]
        tree_dict[tree_key].append(tree_entry)

        # check if it's the tree's masting period
            # if so, spawn a random number of trees
            # TODO double check the logic of this
        #if inc_t % masting_cycle == 0:
            #spawn_some_trees(species, tree_key, tree_entry, tree_dict)
    
        found = True
    
    return found


def determine_tree_stage(age):
    """
        Classify the growth stage of a tree based on how old it is.
        TODO maybe get this to be more specific to different tree types

        AGE IS IN MONTHS   
    """
    if age < 6: 
        # This initial stage, where a seed germinates and becomes a seedling, 
        # usually takes a few weeks to a few months.
        return 'germinating'
    
    elif age < (3*12):
        # The seedling stage is characterized by rapid growth and the development of 
        # a strong root system and several sets of true leaves. This stage can last 
        # anywhere from one to several years, often up to 2-3 years for many tree species.
        return 'seedling'
    
    elif age < (6*12):
        # This stage typically starts when the tree is about 1-3 years old and can last 
        # until the tree is around 5-10 years old. During this period, the tree continues 
        # to grow in height and girth but is not yet mature.
        return 'young'
    
    else:  
        # This stage can vary greatly in length depending on the species, with some trees 
        # maturing in as little as 10-20 years, while others may take several decades.
        return 'mature'


def spawn_some_trees(species, parent_key, parent_entry, tree_dict):
    """
        Takes in the tree information and key from the parent, adds new tree seedlings
        within a specific area and gives them a similar key to the parent
    """

    # For each seedling spawned
        # Create a new key from the parent
        # Get new x and z coordinates
            # Check to make sure that there is not already a tree there
        # add_tree_To_dict() with:
            # information obtained from the tree 
    
    key = create_tree_key(tree_key=parent_key, spawn_count=1) # spawn count should change with each iter of the for loop
    age = 0
    name = parent_entry[1]
    inc_t = parent_entry[0]
    masting_cycle = parent_entry[10]
    x = random_coordinate()
    z = random_coordinate()

    random_factors = randomize_tree_factors(species)
    tree_dict[key] = [] 
    add_to_tree_dict(species, tree_dict, key, random_factors, [name, x, z], name, masting_cycle, age, inc_t)
    pass

def random_coordinate():
    return random.uniform(0, 1)
    

def tree_dict_to_csv(tree_dict, output_csv_filepath):
    """ 
    Takes in the dictionary of tree data, outputs it as a csv 
    
    """
    with open(output_csv_filepath, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Iterate through each key in the dictionary
        for key in tree_dict:
            # Write each subarray (list of values) as a new row in the CSV
            for subarray in tree_dict[key]:
                csv_writer.writerow([key] + subarray)
    pass


def threepg(climatedata_filename, speciesdata_filename, outputdata_filename="output.csv", t=60):

    #outputdata_filename = 'test_data/TEST_THREEPG_OUTPUT.csv'
    num_trees = 100
    height_dbh, tree_list = compute(climatedata_filename, speciesdata_filename, t, num_trees)
    print(f"height_dbh: {tree_list}")
    # so we have the height, the dbh for each species, and now we need to plot the trees and combine the two.
    # We'll need to randomize the actual height and dbh for each individual tree
    
    print("\n===== PLOTTING TREE COORDINATES =====\nExit the scatter plot window to continue...\n")
    tree_coordinates = init_trees_dont_write_yet(speciesdata_filename, plot=False, num_trees=num_trees) # returns [name, x, z]

    tree_output = create_tree_list(tree_coordinates, tree_list,t)
    # for each of the 3-PG data entries in the height_dbh

    tree_dict_to_csv(tree_output, outputdata_filename)

    print("\n===== CALCULATIONS FINISHED ===== ")
    print(f"Data for use in Blender outputted to: {outputdata_filename}")

    #return outputdata_filename