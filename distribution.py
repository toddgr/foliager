"""
File: distribution.py
Author: Grace Todd
Date: January 20, 2024
Description: Will probably change the name of this file later. This needs more proper organization.
            For the moment, though, this file will hold the values and calculations derived from 
            Thompson (https://ir.library.oregonstate.edu/concern/parent/x920g532g/file_sets/9p290j47b)
            and her work with 3-PG.
"""

mystery = None # for formulas I don't know the answer to yet

phys_mod_method = mystery
fd = mystery # defined in calculate_phys_mod
ftheta = mystery
fa = mystery
d = mystery #mean daytime vapor pressure deficit
E = mystery
kd = mystery
soil_water = mystery
max_soil_water = mystery

def calculate_phys_mod():
    phys_mod = 1.
    if phys_mod_method:
        #limiting phys_mod. uses only most limiting of vpd and soil water mods
        lim = fd if fd <= ftheta else ftheta
        phys_mod = fa * lim
    
    fd = pow(E, (-kd * d))

    # soil water mod, ftheta
    c_theta = mystery
    n_theta = mystery # both of these are empirical species specific values
    base1 = ((1 - soil_water)/max_soil_water)/c_theta
    ftheta = 1./(1. + pow(base1, n_theta))
    
def calculate_temp_mod():
    # do this next
    pass

#FORMULAS AND EQUATIONS

phys_mod = calculate_phys_mod()    #accounts for the effects of age, vapor pressure deficit, and available soil water
temp_mod = mystery
frost_mod = mystery
nutrient_mod = mystery
maximum_potential_cqe = mystery
co2_mod = mystery

cqe = (maximum_potential_cqe) * phys_mod * temp_mod * frost_mod * nutrient_mod * co2_mod
par = mystery

gpp = cqe * par     #gross primary production