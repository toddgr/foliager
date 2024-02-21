"""
File: 3pg.py
Author: Grace Todd
Date: February 21, 2024
Description: My attempt at converting 3-PG to Python so that I can use it in my calculations and 
             whatnot.
"""

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
    def __init__(self, site_tmax, site_tmin, site_rain, site_solar_rad, site_frost_days):
        self.tmax = site_tmax   # Average maximum temperature for the month
        self.tmin = site_tmin   # Average minimum temperature for the month
        self.rain = site_rain   # Average rainfall for the month
        self.solar_rad = site_solar_rad # Average solar radiation for the month
        self.forst_days = site_frost_days   # Average number of frost days for the month

"""
    ==================== SITE DATA ========================
"""
MYSTERY = None # Using MYSTERY to define variables that I don't know the value of yet.
# monthly climate data
month_data = [Month() for _ in range(13)]
init_month_data = [Month() for _ in range(13)]

# for modding sliders -- what else is this used for?
site_tmax_mod = 0.
site_tmin_mod = 0.
site_rain_mod = 0
site_solar_rad_mod = 0.
site_frost_days_mod = 0.

# temperature- all in degrees C
t_min = MYSTERY # minimun monthly temperature for growth 
t_opt = MYSTERY # Optimum monthly temperature for growth 
t_max = MYSTERY # maximum monthly temperature for growth

# frost
df = MYSTERY # mean number of frost days per month 
kf = MYSTERY # number of days of production lost for each frost day

# CO2 
fcax_700 = MYSTERY # This one is the "assimilation enhancement factor at 700 ppm" "parameter[s] define the species specific repsonses to changes in atmospheric co2"
co2 = MYSTERY # Atmospheric CO2 (ppm) -- number from oregon values from random site, change later

# VPD 
d = MYSTERY # mean daytime VPD
kd = MYSTERY # defines the stomatal response to VPD

# Soil water mod, and other soil stuff
soil_water = MYSTERY # Available soil water
max_soil_water = MYSTERY # Maximum available soil water
n_theta = MYSTERY # "Power of moisture ration deficit" "differences in the relationship between transpiration rate and soil water content for different soil textures"
c_theta = MYSTERY # Moisture ration deficit for fq = 0.5


"""
    ==================== STAND DATA ========================
    This data is about the stand in question. This is largely decided by
    the user of 3PG, as the point is to be able to use this program 
    for whatever your tree stand is. 
"""

# Initial biomasses -- all are in tonnes of dry mass per hectare, or tDM/ha
init_wf = MYSTERY
init_wr = MYSTERY
init_ws = MYSTERY

init_b = MYSTERY # initial dbh
init_sw = MYSTERY   # initiial available soil water

irr = MYSTERY # irrigation (mm/month)
et = MYSTERY # evapotranspiration (mm/month)

# general for GPP
r = MYSTERY # months since beginning of simulation

fr = MYSTERY # fertility rating, ranges from 0 to 1

age0 = MYSTERY # this is the stand's age in years at t = 0
start_month = MYSTERY # this is the number of the month in which the simulation is beginning
start_year = MYSTERY # this is the year the simulation was started. Used for prints only?

physmod_method = MYSTERY # this denotes the method used to calculate physmod. 0 = combo 1= limiting
agemod_method = MYSTERY # 0 = agemod not used, 1 = agemod used
display_mode = MYSTERY # cones vs textures. Probably won't use this but I'll keep for ref, for now.


"""
    ==================== SPECIES DATA ========================
    Original -- This data is all from Forrester et al. in press, and featured on the 3PDGmix.Data
    Excel sheet. The data is refered to as 
    Since this program deals specifically with Douglas Firs, this data will not change. 

    So... these are the parameters that I either need to a) force the NLP to find data on,
    or b) generalize for the purposes of the program. Also double check that these have constant values
    and aren't computed based on something. I want to give the NLP as few things to look for as possible.

    Eventually, maybe I can automate this so that it reads in these values from a generated CSV, which then assigns it values in the program.
"""

lec = MYSTERY # a light extinction coefficient

p2 = MYSTERY # diameter at breast height at 2cm, used in partitioning ratios
p20 = MYSTERY # diameter at breast height at 20cm, used in partitioning ratios

acx = MYSTERY # species-specific max potential canopy quantum efficiency

sla_1 = MYSTERY # SLA in older stands
sla_0 = MYSTERY # SLA in younger stands
t_sla_mid = MYSTERY # age where SLA = 0.5(sla_0-sla_1)

fn0 = MYSTERY # value of fN when FR = 0
nfn = MYSTERY # power of (1-FR) in fN

tc = MYSTERY # age when canopy closes

max_age = MYSTERY # Max stand age, used in age mod
r_age = MYSTERY # relative age to give fage = 0.5
n_age = MYSTERY # power of relative age in f_age function

# Mean fractions of biomass per tree that is lost when a tree dies -- per pool
mf = MYSTERY
mr = MYSTERY
ms = MYSTERY

# Biomass
yfx = MYSTERY
yf0 = MYSTERY
tyf = MYSTERY
yr = MYSTERY # average monthly root turnover rate (1/month)
nr_min = MYSTERY # minimum root partitioning ratio
nr_max = MYSTERY # maximum root partitioning ratio
m_0 = MYSTERY # m on sites of poor fertility, eg. FR=0

# for mortality
wsx1000 = MYSTERY # value of wsx when n = 1000
nm = MYSTERY # exponent of self-thinning rule

"""
    ================ MISC ===============
"""
cr = 0.47 # conversion ratio for making GPP into NPP

"""
    ==================== 3PG OUTPUTS ========================
"""
n = MYSTERY # trees per square hectare
gpp = MYSTERY # gross primary production
npp = MYSTERY # net primary production
wf = MYSTERY # foliage biomass (Mg/ha which is megagramme/hectare, a megagramme is a tonne)
wr = MYSTERY # root biomass (Mg/ha)
ws = MYSTERY # stem biomass (Mg/ha)
par = MYSTERY # absorption of photosynthetically active radiation
mean_stem_mass = MYSTERY # this comes from the mortality calculations? We think
live_crown_length = MYSTERY # length of live portion of tree foliage
crown_base_height = MYSTERY # how far off ground does the live crown start
b = MYSTERY # mean diameter at breast height, aks B or DBH (cm)
h = MYSTERY # mean total tree height, aka H (m)
hl = MYSTERY # live crown length (m)
k = MYSTERY # crown diameter (m)
ba = MYSTERY # basal area (m^2)
vs = MYSTERY # stand volume (m^3/ha)
gac = MYSTERY # proportion of ground area covered by the canopy