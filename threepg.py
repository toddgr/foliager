"""
File: 3pg.py
Author: Grace Todd
Date: February 21, 2024
Description: My attempt at converting 3-PG to Python so that I can use it in my calculations and 
             whatnot.
"""

import math # for log
from threepg_species_data import parse_species_data
from parse_tree_input import csv_file_to_list
from plot_trees_random import init_trees, init_trees_dont_write_yet
import csv
import random

# So I'm going to start out by using Allison's implementation of a tree struct for the sake of visualization. 
# In the future, though, I'll integrate this with my own tree_class. I jsut don't know how different they will
# be yet, and whether or not it would be efficient to have them as the same class.

class TreeViz:
    """
        For visualizing the trees, originally in C++ code from Allison Thompson
    """
    def __init__(self, x, z, dbh_dev, height_dev, draw) -> None:
        self.position = (x, z)          # X and Z coordinates of the spawn point (?) of the tree
        self.dbh_dev = dbh_dev          # Diameter of breast height
        self.height_dev = height_dev    # height of the tree
        self.draw = draw                # Bool -- either draw or don't draw the tree


class Month:
    """
        Holds important information for visualization based on data from the site about the current month.
    """
    def __init__(self, site_tmax, site_tmin, site_rain, site_solar_rad, site_frost_days, site_soil_water, site_max_soil_water):
        self.tmax = site_tmax   # Average maximum temperature for the month
        self.tmin = site_tmin   # Average minimum temperature for the month
        self.rain = site_rain   # Average rainfall for the month
        self.solar_rad = site_solar_rad # Average solar radiation for the month
        self.frost_days = site_frost_days   # Average number of frost days for the month
        self.soil_water = site_soil_water
        self.max_soil_water = site_max_soil_water

"""
    ==================== SITE DATA ========================
"""
MYSTERY = None # Using MYSTERY to define variables that I don't know the value of yet.
SPECIES_SPECIFIC = None # Don't want to hard code Douglas fir values for tree parameters


# monthly climate data
# month_data = [Month() for _ in range(13)]
# init_month_data = [Month() for _ in range(13)]
# climatedata_filename = 'test_data/douglas_fir_climate_data.csv'
# speciesdata_filename = 'test_data/douglas_fir_species_data.csv'
# speciesdata_list = parse_species_data(speciesdata_filename)
# douglasfir = speciesdata_list[0] # Using Douglas fir as a starting pooint bc we know all the values
# month_data, init_month_data = read_climate_data(filename)

# for modding sliders -- what else is this used for?
site_tmax_mod = 0.
site_tmin_mod = 0.
site_rain_mod = 0
site_solar_rad_mod = 0.
site_frost_days_mod = 0.

# temperature- all in degrees C
# t_min = douglasfir.t_min # minimun monthly temperature for growth 
# t_opt = douglasfir.t_opt # Optimum monthly temperature for growth 
# t_max = douglasfir.t_max # maximum monthly temperature for growth

# frost
# df = douglasfir.df # mean number of frost days per month 
# kf = douglasfir.kf # number of days of production lost for each frost day

# CO2 
# fcax_700 = douglasfir.fcax_700 # This one is the "assimilation enhancement factor at 700 ppm" "parameter[s] define the species specific repsonses to changes in atmospheric co2"
co2 = 350 # Atmospheric CO2 (ppm) -- number from oregon values from random site, change later

# VPD 
d = 1. # mean daytime VPD --> SLIDER 0.5 - 2.
# kd = douglasfir.kd # defines the stomatal response to VPD

# Soil water mod, and other soil stuff
# soil_water = douglasfir.soil_water # Available soil water
# max_soil_water = douglasfir.max_soil_water # Maximum available soil water
# n_theta = douglasfir.n_theta # "Power of moisture ration deficit" "differences in the relationship between transpiration rate and soil water content for different soil textures"
# c_theta = douglasfir.c_theta # Moisture ration deficit for fq = 0.5


"""
    ==================== STAND DATA ========================
    This data is about the stand in question. This is largely decided by
    the user of 3PG, as the point is to be able to use this program 
    for whatever your tree stand is. 
"""

# Initial biomasses -- all are in tonnes of dry mass per hectare, or tDM/ha
init_wf = 7.
init_wr = 9.
init_ws = 20.

init_b = 9 # initial dbh-- was 18
init_sw = 200   # initiial available soil water

#irr = MYSTERY # irrigation (mm/month).
#et = MYSTERY # evapotranspiration (mm/month).

# general for GPP
fr = 1 # fertility rating, ranges from 0 to 1

age0 = 5 # this is the stand's age in years at t = 0
start_month = 5 # this is the number of the month in which the simulation is beginning
start_year = 2024 # this is the year the simulation was started. Used for prints only?

physmod_method = 0 # this denotes the method used to calculate physmod. 0 = combo 1= limiting
agemod_method = 0 # 0 = agemod not used, 1 = agemod used
display_mode = 0 # cones vs textures. Probably won't use this but I'll keep for ref, for now.

cr = 0.47 # conversion ratio for making GPP into NPP

"""
    ==================== 3PG OUTPUTS ========================
n = MYSTERY # trees per square hectare
#gpp = MYSTERY # gross primary production
#npp = MYSTERY # net primary production
#wf = MYSTERY # foliage biomass (Mg/ha which is megagramme/hectare, a megagramme is a tonne)
#wr = MYSTERY # root biomass (Mg/ha)
#ws = MYSTERY # stem biomass (Mg/ha)
#par = MYSTERY # absorption of photosynthetically active radiation
#mean_stem_mass = MYSTERY # this comes from the mortality calculations? We think
#live_crown_length = MYSTERY # length of live portion of tree foliage
#crown_base_height = MYSTERY # how far off ground does the live crown start
b = MYSTERY # mean diameter at breast height, aks B or DBH (cm)
h = 8 # mean total tree height, aka H (m)
hl = MYSTERY # live crown length (m)
k = SPECIES_SPECIFIC # crown diameter (m)
ba = MYSTERY # basal area (m^2)
vs = MYSTERY # stand volume (m^3/ha)
gac = MYSTERY # proportion of ground area covered by the canopy
"""

def read_climate_data_original(filename):
    """
        Reads in a CSV file that contains data on the monthdata
    """
    month_data = []  # Assuming monthdata is a list of objects with attributes site_tmax, site_tmin, etc.
    init_month_data = []  # Assuming initmonthdata is also a list of objects with similar attributes

    with open(filename, 'r') as fp:
        i = 1
        for line in fp:
            fields = line.strip().split(',')

            month_data.append(Month(
                site_tmax=float(fields[0]),
                site_tmin=float(fields[1]),
                site_rain=float(fields[2]),
                site_solar_rad=float(fields[3]),
                site_frost_days=float(fields[4])
            ))

            init_month_data.append(Month(
                site_tmax=month_data[i].site_tmax,
                site_tmin=month_data[i].site_tmin,
                site_rain=month_data[i].site_rain,
                site_solar_rad=month_data[i].site_solar_rad,
                site_frost_days=month_data[i].site_frost_days
            ))
            # print(i)
            i += 1

    return month_data, init_month_data

def read_climate_data(file_path):
    """
        Reads in a CSV file that contains data on the monthdata
    """
    month_data = []  # Assuming monthdata is a list of objects with attributes site_tmax, site_tmin, etc.
    init_month_data = []  # Assuming initmonthdata is also a list of objects with similar attributes

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        i = 0
        for row in reader:
            month_data.append(Month(
                site_tmax = float(row['tmax']),
                site_tmin = float(row['tmin']),
                site_rain = float(row['rain']),
                site_solar_rad = float(row['solar_rad']),
                site_frost_days = float(row['frost_days']),
                site_soil_water = float(row['soil_water']),
                site_max_soil_water = float(row['max_soil_water'])
            ))

            init_month_data.append(Month(
                site_tmax=month_data[i].tmax,
                site_tmin=month_data[i].tmin,
                site_rain=month_data[i].rain,
                site_solar_rad=month_data[i].solar_rad,
                site_frost_days=month_data[i].frost_days,
                site_soil_water=month_data[i].soil_water,
                site_max_soil_water=month_data[i].max_soil_water
            ))
            i = i + 1
    return month_data, init_month_data

def parse_env_data(file_path):
    """ Parses through the environment data for the forest
        (inlcudes both climate data and stand data) to be 
        used in 3-PG """
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
    We're basically just assigning and calculating values for all of the globals that we defined above. 
    Now that I think of it... breaking this up might help to optimize the proces. Maybe.
"""
def compute(environment_data_filename, speciesdata_filename, outputdata_filename, t):
    """
        Takes in climate data, species data, time in months since beginning of simulation
        Computes the outputs for the 3PG algorithm
    """
    E = 2.718
    PI = 3.1415
    d = 0.8
    n = 1200 # number of trees per square hectare
    speciesdata_list = parse_species_data(speciesdata_filename)
    environment = parse_env_data(environment_data_filename)
    height_dbh_list = []
    for species in speciesdata_list:
        #print(f"SPECIES: {species.name}, max soil water = {species.max_soil_water}, soil_water = {species.soil_water}")
        month_data, init_month_data = read_climate_data(environment_data_filename)
        # values of biomass pools that will be used throughout the incremental calculations
        last_wf = init_wf
        last_ws = init_ws
        last_wr = init_wr

        last_sw = init_sw

        delta_n = 0 # number of trees that died last month

        # setting initial b from user input initial b so that it can be used to compute WF
        # Fix this so no user input?
        b = 18

        for inc_t in range(t+1): # t that will be used as an iterator throughout the incremental calculations
            current_month = (start_month + inc_t) % 12
            if current_month == 0:
                current_month = 12

            # compute the PAR/aC mods
            # temperature mod
            ft = 1.
            ta = (month_data[current_month].tmax + month_data[current_month].tmin)/2. # getting mean monthly temp from site data
            if (ta > species.t_max) or (ta < species.t_min):
                # outside of growth range -> 0
                ft = 0.
            else:
                # inside of growth range
                base = (ta - species.t_min / (species.t_opt - species.t_min) * (species.t_max - ta)/(species.t_max - species.t_opt))
                exp = (species.t_max - species.t_opt)/(species.t_opt - species.t_min)
                ft = pow(base, exp)

            # frost mod
            df = month_data[current_month].frost_days
            ff = 1. - species.kf * (df/30.)

            # nutrition mod
            fn = 1. - (1. - species.fn0) * pow((1. - fr), species.nfn)

            # C02 mod
            fc = 1
            fcax = species.fcax_700/(2. - species.fcax_700) # we're not exactly sure that this does
            fc = fcax * co2/(350. * (fcax - 1.) + co2) #TODO fix this later

            # phys mod stuff --> made from a combo of fd, ftheta, and age mod that can be changed in glui
            # TODO change this so that it can't be modified from the GLUI
            # vapor pressure deficit (VPD) mod
            fd = pow(E, (-species.kd * d))

            # soil water mod
            base1 = ((1. - month_data[current_month].soil_water)/month_data[current_month].max_soil_water)/species.c_theta
            ftheta = 1./(1. + pow(base1, species.n_theta))

            # age mod --> used if denoted in glui
            # TODO maybe just not use this?
            fa = 1.
            if agemod_method:
                age_base = ((age0 + (inc_t / 12.))/species.max_age)/species.r_age
                fa = 1. / (1. + pow(age_base, species.n_age))
            
            # calculating phys mod
            physmod = 1.
            if physmod_method:
                # limiting physmod, uses only most limiting of vpd and soil water mods
                lim = fd if fd <= ftheta else ftheta
                physmod = fa * lim
            else:
                # combo physmod, both vpd and soil water mods influence physmods
                physmod = fa * fd * ftheta
            
            # SLA -- specific leaf area
            exp1 = pow(((age0 * 12.) + inc_t)/species.t_sla_mid, 2.)
            sla = species.sla_1 + (species.sla_0 - species.sla_1) * pow(E, (-1 * math.log(2.) * exp1))

            # leaf area index (m^2 / m^2)
            l = 0.1 * sla * last_wf

            # GAC --> percentage of ground area covered by canopy
            if age0 + inc_t / 12 < species.tc:
                gac = (age0 + inc_t / 12) / species.tc
            else:
                gac = 1.
            
            # light absorption --> absorption photosynthetically active radiation (PAR)
            # Often called o/pa
            e_exp = (-species.k * l)/gac
            par = (1. - pow(E, e_exp)) * 2.3 * gac * month_data[current_month].solar_rad # the delta t is excluded because it will always be 1
        
            # Computing GPP and NPP
            gpp = ft * ff * fn * fc * physmod * species.acx * par
            npp = gpp * cr

            # Partitioning ratios
            # computing m --> linear function of FR (fertility rating)
            m = species.m_0 + ((1. - species.m_0) * fr)

            # computing the root partitioning ratio
            nr = (species.nr_min * species.nr_max) / (species.nr_min + ((species.nr_max - species.nr_min) * m * physmod))

            # computing np and ap, which are used to calculate pfs
            np = (math.log(species.p20/species.p2))/math.log(10.) # equation A29
            ap = species.p2/(pow(2., np)) # equation A29

            # computing pfs
            b = 18
            pfs = ap * pow(b, np)
            #print(f"pfs:{pfs}, ap:{ap}, b:{b}, np:{np}\npfs = ap * pow(b, np)")

            # getting remaining partitioning ratios
            nf = (pfs * (1. - nr))/(1. + pfs)
            ns = (1. - nr)/(1. + pfs)
            #print(f"nr:{nr}, pfs:{pfs}")

            # mortality
            # max individual tree stem mass (wsx)
            wsx = species.wsx1000 * pow((1000.0/n), species.nm)

            # print("last_ws:", last_ws)
            # seeing if we need to thin
            while last_ws / n > wsx:
                # need to thin
                n -= 1  # decreasing n
                delta_n += 1 # increasing delta_n counter
                wsx = species.wsx1000 * pow((1000.0/n), species.nm) # recalculating wsx

            # litterfall
            current_age = age0 + t/12
            # according to 3-PG manual, page 33:
                # For deciduous species, the litterfall rates yf0 and yfx may be considered 
                # to be 0 because all of the foliage is lost at the end of the growing season anyway.
            if species.q_deciduous_evergreen == ['deciduous'] and (species.yf0 == 0 or species.yfx == 0):
                yf = 0  # otherwise we get a divide by zero
            else: 
                lf_exp = -(current_age/species.tyf) * math.log(1.0 + species.yfx/species.yf0)
                yf = (species.yfx * species.yf0)/(species.yf0 + (species.yfx - species.yf0) * pow(E, lf_exp))

            # Computing biomass
            # using init_wx and just plain n here because this is designed to be 
            # calculated from any point in the simulation.

            # doing this on a monthly time step

            # setting current = to last month's
            curr_wf = last_wf
            curr_ws = last_ws
            curr_wr = last_wr

            #print(f"curr_ws (part 1): {curr_ws}")

            # incrementing the current using last month's values
            curr_wf += (nf * npp) - (yf * last_wf) - (species.mf * (last_wf / n) * delta_n)
            curr_wr += (nr * npp) - (species.yr * last_wr) - (species.mr * (last_wr / n) * delta_n)
            
            
            #print(f"the complexificaiton may begin.\nns:{ns}, npp:{npp}, species.yr:{species.yr}, last_wr:{last_wr},species.mr:{species.mr},n:{n}, delta_n:{delta_n}")
            curr_ws += (ns * npp) - (species.ms * (last_ws / n) * delta_n)

            #print(f"curr_ws (part 2): {curr_ws}")

            # making the current into last month's for the next month
            last_wf = curr_wf
            last_ws = curr_ws
            last_wr = curr_wr

            delta_n = 0 # resetting delta_n

            # Computing miscellaneous parameters
            # these are all just for printing out, not viz...
            """NOTE: for all the below stand level variables, the C parameter has been left out. 
                C is a competition index and is only applicable to mixed species stands, which this
                implementation does not cover. However, if you were to adapt this implementation to 
                account for mixed species stands, it would be easy to add in the C parameter here
                in the future, as described in section 11.11 of Forrester's User Manual. rh (relative
                height) has also been left out for the same reason.
                TODO: Add in the C parameter here
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

            # calculating b from mean individual stem mass (inversioon of A65 of user manual)
            iws = last_ws / n # individual stem mass
            b = pow(iws/aws, (1.0/nws)) *100

            # bias correction to adjust b
            # TODO implement later?

            # mean tree height
            h = 1.3 + ah * pow(E, (-nhb/b)) + nhc * b # for single tree species
            #h = ah * pow(b, nhb) # for data from individual tree data, not used

            # live crown length
            hl = 1.3 + ahl * pow(E, (-nhlb/b)) + nhlc * b # for single tree species
            #hl = ahl * pow(b, nhlb) * pow(hl, nhll) # for data from individual tree data, not used

            # crown diameter
            crown_diameter = ak * pow(b, nkb) * pow(h, nkh)

            # basal area
            ba = (PI * b * b)/40000

            # stand volume
            vs = av * pow(b, nvb) * pow(h, nvh) * pow(b * b * h, nvbh) * n

        # setting final biomass values
        wf = last_wf
        ws = last_ws
        wr = last_wr

        # some test prints
        print(f"\n=== t={t} for {species.name} ===")
        #print(f"FINAL BIOMASS VALUES\nwf: {wf}\nws: {ws}\nwr: {wr}")
        print(f"Live crown length: {hl}\ncrown diameter: {crown_diameter}\nbasal area: {ba}\nstand volume: {vs}")
        #plot the trees
        total_height = h # mean tree height
        live_crown_length = hl # distance between the top live foliage and the lowest live foliage
        dbh = math.sqrt((4 * ba) / math.pi) # trunk of the standing tree
        height_dbh_list.append([species.name, species.q_tree_form, total_height, dbh, live_crown_length, crown_diameter])
    return height_dbh_list
            
# def init_trees():
#     # base this off of a combination of allison's code, as well as my random generation for scatter plots
#     # I have the code where it writes the coordinates to a csv file, but I didn't push it from my pc so we will have to wait
#     # take in the csv, parse each tree species collaection of coordinates, give the trees random height and breast height and stuff
#     # I migth not even want to take in the csv-- i might want to just take the proof of concept and 
#     # recreate it here
#     pass

def create_tree_list(tree_coordinates, height_dbh):
    """ Creates the list/dict of tree information for every single tree in the forest. 
        Taking it out of the 3PG function for better readability and also to isolate the 
        data structure so I can mess with it a little bit.

        the old structure of this: 
        ['name', 'q_tree_form', 'x', 'z', 'height', 'dbh', 'lcl', 'c_diameter']
        in list/array form

        The new structure will be a dict with the structure:
        { tree1 :
            [[t, dead, name, q_tree_form, x, z, height, dbh, lcl, c_diameter],
            [t, dead, name, q_tree_form, x, z, height, dbh, lcl, c_diameter],
            [t, dead, name, q_tree_form, x, z, height, dbh, lcl, c_diameter]
            ]
        }

        This is so that we can access multiple instances of the same tree at different time values, and 
        also to make it easier to spawn/kill off trees in an organized way.

        Then, once ALL of the data has been written for all the trees at all the times, then we can write
        it in CSV form, where each tree for each line is written in chronological order.
    """
    tree_output = [['name', 'q_tree_form', 'x', 'z', 'height', 'dbh', 'lcl', 'c_diameter']]

    for tree in tree_coordinates[1:]:
        tree_name = tree[0]
        found = False
        for tree_3pg in height_dbh:
            #species.name, species.q_tree_form, total_height, dbh, live_crown_length, crown_diameter
            tree_name_3pg = tree_3pg[0]
            if tree_name == tree_name_3pg:
                tree_form = tree_3pg[1]

                # assign slightly randomized values to the height and dbh
                factor_height = float(tree_3pg[2]) / 4
                random_height_offset = random.uniform(-factor_height, factor_height)
                new_height = float(tree_3pg[2]) + random_height_offset

                factor_dbh = float(tree_3pg[3]) / 4
                random_dbh_offset = random.uniform(-factor_dbh, factor_dbh)
                new_dbh = float(tree_3pg[3]) + random_dbh_offset

                factor_lcl = float(tree_3pg[4]) / 4
                random_lcl_offset = random.uniform(-factor_lcl, factor_lcl)
                new_lcl = float(tree_3pg[4]) + random_lcl_offset

                factor_c_diam = float(tree_3pg[5]) / 4
                random_c_diam_offset = random.uniform(-factor_c_diam, factor_c_diam)
                new_c_diam = float(tree_3pg[5]) + random_c_diam_offset

                # append it to the tree_coordinate entry
                # [name, q_tree_form, , z, height, dbh, lcl, c_diameter]
                tree_output.append([tree_name, tree_form, tree[1], tree[2], new_height, new_dbh, new_lcl, new_c_diam])

                found = True
                break
        if not found:
            print(f"Uh oh! Tree data for {tree_name} could not be found.")

    return tree_output

def tree_dict_to_csv(tree_dict, output_csv_filepath):
    """ Takes in the dictionary of tree data, outputs it as a csv
        Example format:
        Tree name, 0, dead, name, q_tree_form, x, z, height, dbh, lcl, c_diameter
        Tree name, 1, dead, name, q_tree_form, x, z, height, dbh, lcl, c_diameter
        ...
        Tree name2, 0, dead, name, q_tree_form, x, z, height, dbh, lcl, c_diameter
        Tree name2, 1, dead, name, q_tree_form, x, z, height, dbh, lcl, c_diameter
        ..."""
    
    with open(output_csv_filepath, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(tree_dict)
    pass


def threepg(climatedata_filename, speciesdata_filename, outputdata_filename="output.csv"):

    # TODO: convert this to its own function to be used in foliager main
    #outputdata_filename = 'test_data/TEST_THREEPG_OUTPUT.csv'
    height_dbh = compute(climatedata_filename, speciesdata_filename, outputdata_filename, 10)
    # print(f"height_dbh: {height_dbh}")
    # so we have the height, the dbh for each species, and now we need to plot the trees and combine the two.
    # We'll need to randomize the actual height and dbh for each individual tree
    
    print("\n===== PLOTTING TREE COORDINATES =====\nExit the scatter plot window to continue...\n")
    tree_coordinates = init_trees_dont_write_yet(speciesdata_filename, plot=True) # returns [name, x, z]
    
    tree_output = create_tree_list(tree_coordinates, height_dbh)
    # for each of the 3-PG data entries in the height_dbh

    tree_dict_to_csv(tree_output, outputdata_filename)

    print("\n===== CALCULATIONS FINISHED ===== ")
    print(f"Data for use in Blender outputted to: {outputdata_filename}")

    #return outputdata_filename