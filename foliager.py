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
initial_attributes = "Common_name,scientific_name,leaf_shape_(oval/truncate/elliptical/lancolate/linear/other),canopy_density_(very_thin/thin/medium/dense/very_dense),deciduous_or_evergreen,leaf_color_(green),tree_form_(round/spreading/pyramidal/oval/conical/vase/columnar/open/weeping/irregular),tree_roots_(deep/shallow),habitat_(polar/temperate/dry/continental/tropical/subtropical/subcontinental/mediterranean/alpine/arid/subarctic/subalpine),bark_texture_(smooth/lenticels/furrows/ridges/cracks/scales/strips),bark_color_(gray/white/red/brown)\n"

import re
from parse_tree_input import  csv_file_to_string

from tree_class import Tree, TreeList
from plot_trees_random import init_trees
from threepg_species_data import parse_species_data, get_tree_names
from parse_csv_file import *
from threepg import threepg
from param_estimator import estimate_tree_list
#from blender_place_trees import gen_trees_in_blender

def ask_nlp(prompt, model="gpt-3.5-turbo"):
    # Ask ChatGPT a question, return the answer.
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content   

def make_valid_filename(input_string):
    extension = "_foliage.csv"
    cleaned_string = re.sub(r'[^\w\s-]', '', input_string)  # Remove special characters except for spaces and hyphens
    cleaned_string = re.sub(r'\s+', '_', cleaned_string)    # Replace consecutive spaces with a single underscore
    cleaned_string = cleaned_string.strip('_-')

    if not cleaned_string:
        cleaned_string = 'untitled'

    max_length = 255 - len(extension)
    cleaned_string = cleaned_string[:max_length]

    return cleaned_string + extension

def generate_prompt():
    attributes = csv_file_to_string("parameters/default_tree_chart.csv")
    prompt = "Output an unnumbered list of foliage types in CSV format that can be found in "
    location = input("Enter the climate, city, or area:")
    prompt += location + " with the following attributes:" + attributes
    prompt += attributes
    #print(prompt)
    print("Generating foliage list for ", location, "...")

    return prompt, location

if __name__ == '__main__':
    asknlp = False       # If we want to generate new data --> usage is limited

    climate_data_filepath = "test_data/douglas_fir_climate_data.csv"    #temporary
    param_est_output = "test_data/param_est_output.csv"                 # in-between file for parameter estimation
    threepg_output_filepath = "test_data/OUTPUT_DATA.csv"
    knowledge_base = "test_data/species_data_kb.csv"
 
    if asknlp: 
        prompt, location = generate_prompt()
        response = ask_nlp(prompt) #commented out to save query time
        #print(response)
        # Write the NLP response to a csv file
        nlp_response_filepath = "test_data/" + make_valid_filename(location)
        with open(nlp_response_filepath, 'w') as file:
            file.write(initial_attributes)
            file.write(response)
            print("Writing to file ", nlp_response_filepath)
            # Now to parse input into Tree and TreeList objects
        foliage_list = parse_csv_file(nlp_response_filepath)

    else:
        # use last NLP prompt (that I know works)
        nlp_response_filepath = "test_data/portland_oregon_foliage.csv"
        print(f"===== NLP NOT USED. =====\n Parsing tree data from {nlp_response_filepath}...")
        foliage_list = parse_csv_file(nlp_response_filepath)


    print("\n===== ESTIMATING PARAMETERS for the following trees: ===== ")
    for tree in foliage_list:
        print(tree.name)

    estimate_tree_list(foliage_list, knowledge_base, param_est_output)
    #gen_trees_in_blender(coordinates_file) # have to have bpy and stuff for this line 

    print("\n\n ===== CALCULATING 3-PG PARAMETERS NOW =====")
    threepg(climate_data_filepath, param_est_output, threepg_output_filepath)

    