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

# Open the secret key
with open('parameters/secret_key.txt', 'r') as file:
    api_key = file.read()

client = OpenAI(api_key=api_key)

def ask_llm(prompt, model="gpt-4o-mini"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model, messages=messages, temperature=0)
    return response.choices[0].message.content

def get_species_data(location):
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
    species_header = 'name, scientific name, leaf_shape, canopy_density, deciduous_evergreen, leaf_color, tree_form, tree_roots, \
habitat, bark_texture, bark_color, masting_cycle, seeding_age'

    # the full LLM prompt
    species_prompt = "Only output an unnumbered list of tree types in CSV format that can be found in" + location + "with the \
following attributes:" + species_attributes + "\n Please include the headers \"" + species_header + "\" at the beginning of the output."
    
    species_data = ask_llm(species_prompt)
    clean_species_data = species_data.replace('```', '').strip()
    
    print(species_prompt)
    print("\n===========================================\n")
    print(clean_species_data)

    return clean_species_data

def get_climate_data(location):
    pass


if __name__ == '__main__':
    # 1. Prompt user for a climate, city, or location:
    location = input("Enter the climate, city, or area:")

    # 2. LLM generates tree data, outputs two strings:
    species_data = get_species_data(location)
    climate_data = get_climate_data(location)

    # 3. A forest is created:
    
    # 4. Forest information and tree dimensions are passed on to Blender:
    # ref: https://blender.stackexchange.com/questions/1365/how-can-i-run-blender-from-command-line-or-a-python-script-without-opening-a-gui