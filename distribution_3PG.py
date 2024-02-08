"""
File: distribution_3PG.py
Author: Grace Todd
Date: January 22, 2024
Description: Will probably change the name of this file later. This needs more proper organization.
            For the moment, though, this file will hold the values and calculations derived from 
            3-PG https://3pg.forestry.ubc.ca/files/2014/04/3PGdescription-1st-Lecture.pdf
"""
import math

mystery = None # as in, idk what these values are yet lmao
depends_on_the_environment = mystery # variables that depend on the environment info
depends_on_the_species = mystery 
depends_on_the_stand = mystery


# From the slides:

def temp_growth_modifier():
    # Temperature growth modifier
    t_a = depends_on_the_environment   # mean monthly daily temperature
    t_min = depends_on_the_species # minimum temperature for growth
    t_opt = depends_on_the_species # optimum temperature for growth
    t_max = depends_on_the_species # maximum temperature for growth

    f_t_base = ((t_a - t_min) / (t_opt - t_min)) * ((t_max - t_a) / (t_max - t_opt))
    f_t_exp = ((t_max - t_opt) / t_opt - t_min)

    f_t = pow(f_t_base, f_t_exp)
    return f_t

def frost_growth_modifier():
    # Frost growth modifier
    d_f = depends_on_the_environment   # number of frost days in month
    k_f = depends_on_the_species   # number of days of production lost for each day of frost

    f_f = 1 - k_f * (d_f / 30)

    return f_f

def soil_water_growth_modifier():
    theta = depends_on_the_environment # curent available soil water
    theta_x = depends_on_the_environment   # maximum available soil water
    c_theta = depends_on_the_environment   # relative water deficit for 50% reduction
    n_theta = depends_on_the_environment   # power determining shape of soil water response

    base = (1 - theta / theta_x) / c_theta
    f_sw = 1 / (1 + pow(base, n_theta))
    
    return f_sw

def vpd_growth_modifier():
    d = mystery     # current vapor pressure deficit
    k_d = mystery   # strength of VPD response
    
    f_vpd = pow(e, -k_d * d)

    return f_vpd

def age_related_growth_modifier():
    t = depends_on_the_stand  # current stand age
    t_x = depends_on_the_species   # likely maximum stand age
    r_age = mystery # relative stand age for 50% growth reduction
    n_age = depends_on_the_species # power determining strength of growth reduction

    base = t / (r_age * t_x)
    f_age = 1 / (1 + pow(base, n_age))
    return f_age
    
def root_partitioning():
    m_0 = mystery
    FR = mystery # double check what this is
    m = m_0 + (1 - m_0) * FR
    n_rx = depends_on_the_species # root partitioning under very poor conditions
    n_rn = depends_on_the_species # root partitioning under optimal conditions

    n_r = (n_rx * n_rn) / (n_rn + (n_rx - n_rn) * m * phi)
    return n_r

def litter_fall_rate():
    t = mystery
    gamma_f0 = depends_on_the_species # litter-fall rate at age 0
    gamma_fx = depends_on_the_species # maximum litter-fall rate
    t_gammaf = mystery # age when gamma_f = 0.5 * (gamma_f0 + gamma_fx)
    k = (1 / t_gammaf) * math.log(1 + (gamma_fx / gamma_f0))
    gamma_f = (gamma_fx * gamma_f0) / (gamma_f0 + (gamma_fx - gamma_f0) * pow(e, -k * t))

    return gamma_f

# Growth modifiers in 3-PG, varies between 0 (total limitation) and 1 (no limitation)
f_vpd = vpd_growth_modifier()           # vapor pressure deficit
f_sw = soil_water_growth_modifier()            # soil water
f_t = temp_growth_modifier()             # temperature
f_f = frost_growth_modifier()             # frost
f_n = mystery             # site nutrition
f_age = age_related_growth_modifier()           # stand age


# Calculating intercepted radiation
e = math.e # I'm assuming this is the math e, actually
k = mystery # (1 / t_gammaf) * math.log(1 + (gamma_fx / gamma_f0))
L = mystery
q_zero = mystery
q_int = (1 - pow(e, -k*L)) * q_zero # intercepted radiation


# Gross Canopy Production
alpha_cx = mystery
alpha_c = f_t * f_f * f_n * min(f_vpd, f_sw) * f_age * alpha_cx # canopy quantum efficiency, (mol mol^-1)
phi = min(f_vpd, f_sw) * f_age
p_g = alpha_c * q_int


# Net Canopy Production
y = 0.47 # This is a contentious assumption, which greatly simplifies treatment of respiration
p_n = y * p_g   # Net canopy production

# Biomass partitioning
w_f = depends_on_the_species # foliage
w_s = depends_on_the_species # above-ground woody tissue
w_r = depends_on_the_species # roots

a = 20 #cm
B = 2
n = mystery
p_fs = a * pow(B, n)

n_r = root_partitioning() # root partitioning rate, depends on growth conditions and stand DBH
n_s = (1 - n_r) / (1 + p_fs) # above-ground woody tissue partitioning rate, depends on growth conditions and stand DBH
n_f = p_fs * n_s # foliage partitioning rate, depends on growth conditions and stand DBH
p_fs = n_f / n_s # = a * B^n, where B is diameter at breast height determined from an allometric 
                 # relationship between stem mass and B
                 # a, b are coefficients determined from p_fs at B = 2 and 20 cm
p_n = mystery

gamma_f = litter_fall_rate() # litter fall
gamma_r = 0.015 # root-turnover month^-1
gamma_s = 0.2

delta_w_f = (n_f * p_n) - (gamma_f * w_f)
delta_w_r = (n_r * p_n) - (gamma_r * w_r)
delta_w_s = n_s * p_n

# Stomatal conductance
g_cx = depends_on_the_species # maximum canopy conductance

L_gc = mystery # LAI at maximum conductance
g_c = g_cx * phi * min(L / L_gc, 1)
