"""
File: main.py
Author: Grace Todd
Date: September 17, 2024
Description: This file prepares data for forest generation based on user input.

            WHEN THIS FILE IS RUN:
            1. Prompts user for a climate / city / location
                (e.g. High Desert / Corvallis, Oregon / Amazon Rainforest)
            2. LLM (GPT 4o mini, for now) generates data about user input, including
                trees found in that area, as well as some general information about
                each tree species
            3. A forest is created with the tree species in mind:
                - Information about each tree is used to estimate tree growth parameters
                - Trees of each species are given coordinates in the forest space, in addition
                to specific dimensions for each tree
            4. Forest information and tree dimensions are passed on to Blender, where the
                forest will be generated.
"""

from openai import OpenAI
from create_forest import *

# Open the secret key
with open('parameters/secret_key.txt', 'r') as file:
    api_key = file.read()

client = OpenAI(api_key=api_key)

def ask_llm(prompt, model="gpt-4o-mini"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content

def get_species_data(location, print=False):
    """
    Input: Location specified by the user
    Output: Response from LLM, a CSV-style string of tree species and data
            relevant to that location.
    """
    # species attributes: includes units/categories for LLM to follow
    species_attributes = 'common_name,scientific_name,leaf_shape_(oval/truncate/elliptical/lancolate/linear/other),\
canopy_density_(very_thin/thin/medium/dense/very_dense),deciduous_or_evergreen,leaf_color_(green),\
tree_form_(round/spreading/pyramidal/oval/conical/vase/columnar/open/weeping/irregular),tree_roots_(deep/shallow),\
habitat_(polar/temperate/dry/continental/tropical/subtropical/subcontinental/mediterranean/alpine/arid/subarctic/subalpine),\
bark_texture_(smooth/lenticels/furrows/ridges/cracks/scales/strips),bark_color_(gray/white/red/brown),\
average_masting_cycle_(one_value_in_years),minimum_seed_distribution_age_(years)'

    # species header: simpler column names to make the data easier to work with
    species_header = 'name, scientific_name, leaf_shape, canopy_density, deciduous_evergreen, leaf_color, tree_form, tree_roots, \
habitat, bark_texture, bark_color, masting_cycle, seeding_age'

    # the full LLM prompt
    species_prompt = "Only output an unnumbered list of tree types in CSV format that can be found in " + location + " with the \
following attributes:" + species_attributes + "\n Please include the headers \"" + species_header + "\" at the beginning of the output."
    
    species_data = ask_llm(species_prompt)
    clean_species_data = species_data.replace('csv', '').replace('```', '').strip()
    
    if print:
        print("\n======================= SPECIES PROMPT =======================\n")
        print(species_prompt)
        print("\n====================== SPECIES DATA ==========================\n")
        print(clean_species_data)
        print("\n==============================================================\n")

    return clean_species_data

def get_climate_data(location, print=False):
    climate_attributes = "month,tmax(average_maximum_monthly_temperature_celsius),tmin(average_minimum_monthly_temperature_celsius),\
rain(cm),solar_rad(kwh/m2),frost_days(average_number_of_monthly_frost_days),soil_texture(very_coarse_sand/coarse_sand/fine_sand/loamy_sand\
/sandy_loams/fine_sandy_loams/very_fine_sandy_loams/loams/silt_loams/clay_loams/silt_clay_loams/sandy_clay_loams/sandy_clays/silty_clays/clays),\
vpd(average_monthly_vapor_pressure_deficit_kPa)"
    climate_header = "month, tmax, tmin, rain, solar_rad, frost_days, soil_texture, vpd"
    climate_prompt = "Only output the data for monthly values for " + location + " with the following attributes in CSV format: " + \
        climate_attributes + "\n Please include the headers \"" + climate_header + "\" at the beginning of the output."
    
    climate_data = ask_llm(climate_prompt)
    clean_climate_data = climate_data.replace('csv', '').replace('```', '').strip()
    
    if print:
        print("\n===================== CLIMATE PROMPT =========================\n")
        print(climate_prompt)
        print("\n===================== CLIMATE DATA ============================\n")
        print(clean_climate_data)
        print("\n===============================================================\n")

    return clean_climate_data

if __name__ == '__main__':
    # 1. Prompt user for a climate, city, or location:
    #location = input("Enter the climate, city, or area: ")
    location = 'Bend, Oregon'

    # 2. LLM generates tree data, outputs two strings:
    #species_data = get_species_data(location)
    #climate_data = get_climate_data(location)

    climate_data = "month,tmax,tmin,rain,solar_rad,frost_days,soil_texture,vpd\n\
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

    species_data = "name, scientific_name, leaf_shape, canopy_density, deciduous_evergreen, leaf_color, tree_form, tree_roots, habitat, bark_texture, bark_color, masting_cycle, seeding_age\n\
Ponderosa Pine, Pinus ponderosa, linear, medium, evergreen, green, pyramidal, deep, temperate, furrows, brown, 3, 5\n\
Western Juniper, Juniperus occidentalis, other, thin, evergreen, green, irregular, shallow, dry, scales, gray, 5, 7\n\
Quaking Aspen, Populus tremuloides, oval, medium, deciduous, green, round, shallow, temperate, smooth, white, 2, 3\n\
Lodgepole Pine, Pinus contorta, linear, medium, evergreen, green, conical, deep, temperate, furrows, brown, 3, 5\n\
Black Cottonwood, Populus trichocarpa, oval, dense, deciduous, green, spreading, shallow, temperate, smooth, gray, 2, 4\n\
Sugar Pine, Pinus lambertiana, linear, very_dense, evergreen, green, pyramidal, deep, temperate, furrows, brown, 5, 10\n\
Red Alder, Alnus rubra, oval, medium, deciduous, green, open, shallow, temperate, smooth, gray, 2, 3\n\
White Fir, Abies concolor, other, medium, evergreen, green, conical, deep, temperate, smooth, gray, 5, 8"

    # 3. A forest is created:
    forest = create_forest(climate_data, species_data, num_trees = 15)

    # forest.get_climate()
    # forest.climate_list[0].get_month_climate()

    for each_species in forest.species_list:
        each_species.get_basic_info()
    
    # 4. Forest information and tree dimensions are passed on to Blender:
    # ref: https://blender.stackexchange.com/questions/1365/how-can-i-run-blender-from-command-line-or-a-python-script-without-opening-a-gui
    forest.print_tree_list()
    for each_tree in forest.trees_list:
        each_tree.get_tree_info()