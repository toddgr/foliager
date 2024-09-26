"""
File: foliager.py (i.e. main)
Author: Grace Todd
Date: January 17, 2024
Description: Uses ChatGPT to derive a list of foliage from an area specified by the user.
    Implements Tree and TreeList classes to turn list of foliage data into modifiable Python objects
    OpenAI Documentation: https://platform.openai.com/docs/overview
"""

from openai import OpenAI

# Open the secret key
with open('parameters/secret_key.txt', 'r') as file:
    api_key = file.read()

client = OpenAI(api_key=api_key)
initial_species_attributes = "Common_name,scientific_name,leaf_shape_(oval/truncate/elliptical/lancolate/linear/other),canopy_density_(very_thin/thin/medium/dense/very_dense),deciduous_or_evergreen,leaf_color_(green),tree_form_(round/spreading/pyramidal/oval/conical/vase/columnar/open/weeping/irregular),tree_roots_(deep/shallow),habitat_(polar/temperate/dry/continental/tropical/subtropical/subcontinental/mediterranean/alpine/arid/subarctic/subalpine),bark_texture_(smooth/lenticels/furrows/ridges/cracks/scales/strips),bark_color_(gray/white/red/brown),average_masting_cycle_(years),minimum_seed_distribution_age(years)\n"
initial_climate_attributes = "month,tmax(average_maximum_monthly_temperature_celsius),tmin(average_minimum_monthly_temperature_celsius),rain(cm),solar_rad(kwh/m2),frost_days(average_number_of_monthly_frost_days),soil_texture(very_coarse_sand/coarse_sand/fine_sand/loamy_sand/sandy_loams/fine_sandy_loams/very_fine_sandy_loams/loams/silt_loams/clay_loams/silt_clay_loams/sandy_clay_loams/sandy_clays/silty_clays/clays), vpd(average_monthly_vapor_pressure_deficit_kPa)"

import re
from parse_tree_input import  csv_file_to_string

from junk_drawer.plot_trees_random import init_trees
from junk_drawer.threepg_species_data import parse_species_data, get_tree_names
from parse_csv_file import *
from junk_drawer.threepg import threepg
from param_estimator import estimate_tree_list
#from blender_place_trees import gen_trees_in_blender

def ask_nlp(prompt, model="gpt-3.5-turbo"):
    # Ask ChatGPT a question, return the answer.
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content   

def make_valid_filename(input_string):
    extension = ".csv"
    cleaned_string = re.sub(r'[^\w\s-]', '', input_string)  # Remove special characters except for spaces and hyphens
    cleaned_string = re.sub(r'\s+', '_', cleaned_string)    # Replace consecutive spaces with a single underscore
    cleaned_string = cleaned_string.strip('_-')

    if not cleaned_string:
        cleaned_string = 'untitled'

    max_length = 255 - len(extension)
    cleaned_string = cleaned_string[:max_length]

    return cleaned_string + extension

def generate_climate_prompt(location):
    climate_attributes = csv_file_to_string("parameters/default_environment_data.csv")
    
    climate_prompt = "Output a csv providing the data for monthly values for the following: "
    climate_prompt += initial_climate_attributes
    climate_prompt += "for " + location
    climate_prompt += "\n use the headers [month, tmax, tmin, rain, solar_rad, frost_days, soil_texture,vpd]. \
        for soil_texture, choose one of the options provided in the parentheses."

    #print(climate_prompt)
    print(f"Generating climate information for {location} ...")
    return climate_prompt

def generate_species_prompt(location):
    species_attributes = csv_file_to_string("parameters/default_tree_chart.csv")
    species_prompt = "Output an unnumbered list of tree types in CSV format that can be found in "
    species_prompt += location + " with the following attributes:" + species_attributes
    species_prompt += species_attributes

    #print(prompt)
    print(f"Generating foliage list for {location}...")

    return species_prompt

if __name__ == '__main__':
    asknlp = True       # If we want to generate new data --> usage is limited

    param_est_output = "test_data/param_est_output.csv"                 # in-between file for parameter estimation
    threepg_output_filepath = "test_data/OUTPUT_DATA.csv"
    knowledge_base = "test_data/species_data_kb.csv"
 
    if asknlp: 
        location = input("Enter the climate, city, or area:")
        
        species_prompt = generate_species_prompt(location)
        climate_prompt = generate_climate_prompt(location)
        
        # get the species information
        species_response = ask_nlp(species_prompt) #comment out to save query time
        #print(response)

        # Write the foliage data to a csv file
        species_response_filepath = "test_data/" + make_valid_filename(location + " foliage")
        with open(species_response_filepath, 'w') as file:
            file.write(initial_species_attributes)
            file.write(species_response)
            print(f"Writing to file {species_response_filepath}")
            # Now to parse input into Tree and TreeList objects
        foliage_list = parse_csv_file(species_response_filepath)

        # get the climate information
        climate_response = ask_nlp(climate_prompt)

        # Write the climate information to a csv file
        climate_filepath = "test_data/" + make_valid_filename(location + " climate")
        with open(climate_filepath, 'w') as file:
            #file.write(initial_climate_attributes)
            file.write(climate_response)

            print(f"Writing to file {climate_filepath}")

    else:
        # use last NLP prompt (that I know works)
        climate_filepath = "test_data/prineville_oregon_climate.csv"    #temporary
        species_response_filepath = "test_data/prineville_oregon_foliage.csv"
        print(f"===== LLM NOT USED. =====\n Parsing tree data from {species_response_filepath}...")
        foliage_list = parse_csv_file(species_response_filepath)


    print("\n===== ESTIMATING PARAMETERS for the following trees: ===== ")
    for tree in foliage_list:
        print(tree.name)

    estimate_tree_list(foliage_list, knowledge_base, param_est_output)
    

    print("\n\n ===== CALCULATING 3-PG PARAMETERS NOW =====")
    threepg(climate_filepath, param_est_output, threepg_output_filepath)

    