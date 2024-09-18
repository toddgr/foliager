"""
File: create_forest.py
Author: Grace Todd
Date: September 10, 2024
Description: Uses 3-PG to calculate various parameters of a tree, which will be used to generate
             each tree in the simulation at every time interval.
             
             Based on real, scientific data, and uses C++ skeleton framework provided by Allison
             Thompson in her thesis: 
             https://ir.library.oregonstate.edu/concern/honors_college_theses/x920g532g.

             A revised version of 3pg.py

             THE GENERAL IDEA:
             1. Initialize an empty forest
             2. Compute the data for each species of tree found in the forest
             3. Create individual trees from species data & plot them within the forest
             4. Compute spawned/killed trees throughout the simulation
             5. Take the final state of the forest and write to Blender
"""

import math
from Tree import *

E = 2.718
PI = 3.1415

"""
=====================================================================
                                FUNCTIONS
=====================================================================
"""

INIT_DBH = 0. #9 initial dbh-- was 18 TODO determine init_dbh, and what units?

CO2 = 350 # Atmospheric CO2 (ppm) TODO Implement estimated CO2 function taken from NASA data: https://climate.nasa.gov/vital-signs/carbon-dioxide/?intent=121

# general for GPP
FERTILITY_RATING = 1 # fertility rating, ranges from 0 to 1
CONVERSION_RATIO = 0.47 # for making GPP into NPP

START_AGE = 5 # this is the stand's age in years at t = 0
START_MONTH = 1 # this is the number of the month in which the simulation is beginning
START_YEAR = 1960 # this is the year the simulation was started. TODO Used for prints only?

def threepg(forest:Forest, t:int): # TODO init biomasses here
    """
    Input: Forest (climate, species), time interval (in months)
    Output: Updated forest, with specific dimensions for each species
            at the time interval?
    """
    # Initial biomasses -- all are in tonnes of dry mass per hectare, or tDM/ha
    # TODO need to figure out what these values should be, and if they should be
    #       different for each species or even each tree
    init_foliage_biomass = 7.
    init_root_biomass = 9.
    init_stem_biomass = 20.

    # for each of the species in the list:
    for species in forest.species_list:
        # initialize biomass
        last_foliage_biomass = init_foliage_biomass
        last_stem_biomass = init_stem_biomass
        last_root_biomass = init_root_biomass

        num_trees_died = 0 # number of trees that died last month. TODO Use this for killing trees

        # for each month in the time interval:
        for month_t in range(t+1):
            # get the current month, mean temp for the month
            climate = forest.climate_list
            current_month = ((START_MONTH + month_t) % 12)-1 # jan - dec
            if current_month == 0:
                current_month = 11

            # function to calculate co2 levels on earth based on the season and year.
            # estimated from NASA data on Global Climate Change TODO cite source here
            x = START_YEAR + ((START_MONTH + month_t) / 12) # TODO verify this is correct
            co2 = ((98/60) * x - 2885.33) + 3 * math.sin(7 * x)

            env_mods, phys_mod = calculate_mods(climate[current_month], species, co2) # env_mods = ft * ff * fn * fc

            # specific leaf area (SLA)
            exp1 = pow(((START_AGE * 12.) + month_t)/species.t_sla_mid, 2.)
            sla = species.sla_1 + (species.sla_0 - species.sla_1) * pow(E, (-1 * math.log(2.) * exp1))

            # leaf area index (m^2 / m^2)
            leaf_area_index = 0.1 * sla * last_foliage_biomass

            # ground area coverage (GAC) by canopy
            if START_AGE + month_t / 12 < species.tc:
                ground_area_coverage = (START_AGE + month_t / 12) / species.tc
            else:
                ground_area_coverage = 1. # TODO verify this makes sense

            # light absorption --> absorption photosynthetically active radiation (PAR)
            # Often called o/pa
            e_exp = (-species.k * leaf_area_index)/ground_area_coverage
            par = (1 - pow(E, e_exp)) * 2.3 * ground_area_coverage * climate[current_month].solar_rad

            # computing GPP and NPP
            gpp = env_mods * phys_mod * species.acx * par
            npp = gpp * CONVERSION_RATIO

            # partitioning ratios
            # computing m --> linear function of FR (fertility rating)
            m = species.m_0 + ((1. - species.m_0) * FERTILITY_RATING)

            # root partitioning ratio
            root_partition_ratio = (species.nr_min * species.nr_max) / (species.nr_min + ((species.nr_max - species.nr_min) * m * phys_mod))

            # compute np and ap, which are used to calculate pfs TODO what are these
            np = (math.log(species.p20/species.p2))/math.log(10.) # equation A29
            ap = species.p2/(pow(2., np)) # equation A29

            b = 1 # TODO what is b?
            pfs = ap * pow(b, np)

            # getting remaining partitioning ratios
            nf = (pfs * (1. - root_partition_ratio))/(1. + pfs) # TODO foliage partition
            ns = (1. - root_partition_ratio)/(1. + pfs) # TODO soil partition

            # compute litterfall
            current_age = START_AGE + t/12
            # according to 3-PG manual, page 33:
                # For deciduous species, the litterfall rates yf0 and yfx may be considered
                # to be 0 because all of the foliage is lost at the end of the growing season anyway.
            if species.deciduous_evergreen == ['deciduous'] and (species.yf0 == 0 or species.yfx == 0):
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

            # check if we need to thin/kill some trees
            # mortality
            # max individual tree stem mass (wsx)
            max_ind_tree_stem_mass_wsx = species.wsx1000 * pow((1000.0/forest.num_trees), species.nm)
            while last_stem_biomass / forest.num_trees > max_ind_tree_stem_mass_wsx and forest.num_trees > 0:
                # need to thin
                forest.num_trees -= 1  # decreasing n
                num_trees_died += 1 # increasing delta_n counter
                max_ind_tree_stem_mass_wsx = species.wsx1000 * pow((1000.0/forest.num_trees), species.nm) # recalculating wsx

                # calculating b from mean individual stem mass (inversion of A65 of user manual)
            ind_stem_mass_iws = last_stem_biomass / forest.num_trees # individual stem mass
            species.b = pow(ind_stem_mass_iws/species.aws, (1.0/species.nws)) * 100 # TODO what is b?

    return forest


def calculate_mods(curr_climate, species, co2):
    """
    Input: Current climate conditions
    Output: Computed modifiers for use in GPP/NPP computation.
    """
    mean_monthly_temp = (curr_climate.tmax + curr_climate.tmin)/2.
    # temperature mod (ft)
    if (mean_monthly_temp > species.t_max) or (mean_monthly_temp < species.t_min):
        # outside of growth range -> 0
        temp_mod = 0. # TODO temp mod
    else:
        # inside of growth range
        base = (mean_monthly_temp - species.t_min / (species.t_opt - species.t_min) * (species.t_max - mean_monthly_temp)/(species.t_max - species.t_opt))
        exp = (species.t_max - species.t_opt)/(species.t_opt - species.t_min)
        temp_mod = pow(base, exp) #TODO temp mod

    # frost mod
    frost_days = curr_climate.frost_days # aka df
    frost_mod = 1. - species.kf * (frost_days/30.) #TODO frost mod

    # nutrition mod
    nutrition_mod = 1. - (1. - species.fn0) * pow((1. - FERTILITY_RATING), species.nfn) # TODO nutrition mod

    # CO2 mod
    fcax = species.fcax_700/(2. - species.fcax_700) # the species specific repsonses to changes in atmospheric co2
    co2_mod = fcax * co2/(350. * (fcax - 1.) + co2)

    # physical mod - derived from fd, ftheta
    # vapor pressure deficit (VPD) mod
    vpd_mod = pow(E, (-species.kd * curr_climate.vpd)) # TODO VPD mod may be causing issues

    # soil water mod
    base1 = ((1. - curr_climate.soil_water)/curr_climate.max_soil_water)/species.c_theta
    soil_water_mod = 1./(1. + pow(base1, species.n_theta))

    phys_mod = vpd_mod * soil_water_mod # TODO verify we don't need fa (age_mod)

    return temp_mod * frost_mod * nutrition_mod * co2_mod, phys_mod


def compute_dimensions(forest):
    """
    Input: Tree class object
    Output: Computed and slightly randomized dimensions for the tree
    TODO the dimensions outputted don't always make sense...
    """

    forest.compute_competition_indices()
    for tree in forest.trees_list:
        species = tree.species

        # === compute dimensions based on parameters ===

        # bias correction to adjust b TODO implement later?

        # mean tree height TODO what is the difference between species formula and individual tree formula?
        #mean_tree_height = 1.3 + species.ah * pow(np.e, (-species.nhb/species.b)) + species.nhc * species.b # for single tree species
        mean_tree_height = species.ah * pow(species.b, species.nhb) * pow(tree.c, species.nhc) # A.61

        # live crown length TODO same thing
        # live_crown_length = 1.3 + species.ahl * pow(np.e, (-species.nhlb/species.b)) + species.nhlc * species.b
        live_crown_length = species.ahl * pow(species.b, species.nhlb) * pow(tree.c, species.nhlc) # A.62

        # crown diameter
        #crown_diameter = species.ak * pow(species.b, species.nkb) * pow(mean_tree_height, species.nkh)
        crown_diameter = species.ak * pow(species.b, species.nkb) * pow(mean_tree_height, species.nkh) * pow(tree.c, 0) # A.63

        # stand volume TODO not used
        #stand_volume = species.av * pow(species.b, species.nvb) * pow(mean_tree_height, species.nvh) * pow(species.b * species.b * mean_tree_height, species.nvbh) * num_trees

        # diameter at breast height
        dbh = np.sqrt((4 * tree.ba) / np.pi) # trunk of the standing trees

        # Assign to tree
        tree.height = tree.generate_from(mean_tree_height)
        tree.lcl = tree.generate_from(live_crown_length)
        tree.c_diam = tree.generate_from(crown_diameter)
        tree.dbh = tree.generate_from(dbh)


def create_forest(climate, species, num_trees=100):
    """
    Input: Filepaths for climate and species
    Output: File containing tree specifications for use in Blender.
    """
    # 1. Initialize forest
    #    read in the climate data
    #    initialize the forest based on climate data
    forest = Forest(climate, species, num_trees)

    # 2. Compute 3-PG data for each initial species
    start_month = 0
    end_month = 12 * 5 # the entire simulation is five years long
    forest = threepg(forest, end_month - start_month)

    # 3. Create individual trees from species data
    forest = plot_trees(forest)
    # Compute dimensions for each tree based on competition index
    compute_dimensions(forest)

    # 5. Write to Blender

    return forest


if __name__ == '__main__':
    # example usage here
    example_climate = "month,tmax,tmin,rain,solar_rad,frost_days,soil_texture,vpd\n\
January,3.5,-6.1,3.8,2.5,12,loams,1.2\n\
February,6.1,-3.9,2.5,3.0,10,loams,1.5\n\
March,10.0,0.5,2.0,4.5,8,loams,1.8\n\
April,14.5,2.5,1.5,5.5,5,loams,2.1\n\
May,19.0,5.0,1.0,6.5,2,loams,2.5\n\
June,24.0,9.0,0.5,7.5,0,loams,2.8\n\
July,30.0,12.0,0.0,8.0,0,loams,3.0\n\
August,29.5,11.5,0.0,7.8,0,loams,2.9\n\
September,24.0,7.5,0.2,6.5,1,loams,2.6\n\
October,16.0,2.0,1.5,4.5,5,loams,2.3\n\
November,8.0,-2.0,3.0,2.5,10,loams,1.9\n\
December,4.0,-5.0,4.0,2.0,12,loams,1.4"

    example_species = "name, scientific_name, leaf_shape, canopy_density, deciduous_evergreen, leaf_color, tree_form, tree_roots, habitat, bark_texture, bark_color, masting_cycle, seeding_age\n\
Ponderosa Pine, Pinus ponderosa, linear, medium, evergreen, green, pyramidal, deep, temperate, furrows, brown, 3, 5\n\
Western Juniper, Juniperus occidentalis, other, thin, evergreen, green, irregular, shallow, dry, scales, gray, 5, 7\n\
Quaking Aspen, Populus tremuloides, oval, medium, deciduous, green, round, shallow, temperate, smooth, white, 2, 3\n\
Lodgepole Pine, Pinus contorta, linear, medium, evergreen, green, conical, deep, temperate, furrows, brown, 3, 5\n\
Black Cottonwood, Populus trichocarpa, oval, dense, deciduous, green, spreading, shallow, temperate, smooth, gray, 2, 4\n\
Sugar Pine, Pinus lambertiana, linear, very_dense, evergreen, green, pyramidal, deep, temperate, furrows, brown, 5, 10\n\
Red Alder, Alnus rubra, oval, medium, deciduous, green, open, shallow, temperate, smooth, gray, 2, 3\n\
White Fir, Abies concolor, other, medium, evergreen, green, conical, deep, temperate, smooth, gray, 5, 8"

    forest = create_forest(example_climate, example_species, num_trees=100)

    forest.get_climate()
    forest.climate_list[0].get_month_climate()

    for each_species in forest.species_list:
        each_species.get_basic_info()

