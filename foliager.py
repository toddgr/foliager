"""
File: foliager.py (i.e. main)
Author: Grace Todd
Date: January 17, 2024
Description: Uses ChatGPT to derive a list of foliage from an area specified by the user.
    Implements Tree and TreeList classes to turn list of foliage data into modifiable Python objects
    OpenAI Documentation: https://platform.openai.com/docs/overview
"""

from openai import OpenAI
client = OpenAI(api_key='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')

import os
import pandas as pd
import time
import re

from parse_tree_input import parse_csv_file, csv_file_to_string

from tree_class import Tree, TreeList
from plot_trees_random import init_trees
from threepg_species_data import parse_species_data, get_tree_names

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
    print(prompt)
    print("Generating foliage list for ", location, "...")

    return prompt, location

if __name__ == '__main__':
    asknlp = False # If we want to generate new data --> usage is limited
    threepg = True # If we want to use 3PG
 
    if asknlp: 
        prompt, location = generate_prompt()
        response = ask_nlp(prompt) #commented out to save query time
        print(response)
        # Write the NLP response to a csv file
        foliage_file = make_valid_filename(location)
        with open(foliage_file, 'w') as file:
            file.write("Name,Growth Rate,Average Lifespan\n")
            file.write(response)
            print("Writing to file ", foliage_file)
            # Now to parse input into Tree and TreeList objects
        foliage_list = parse_csv_file(foliage_file)
        treelist = TreeList(foliage_list)
        print(treelist.get_tree_names())
        print(treelist.get_all_tree_info())
    else:
        if threepg:
            # Douglas Fir Data
            location = 'Portland Oregon'
            coordinates_file = make_valid_filename("douglas fir coordinates")
            foliage_file = "Test_Data/douglas_fir_species_data.csv"
            foliage_list = parse_species_data(foliage_file) #Name, Growth Rate, Average Lifespan
            treelist = get_tree_names(foliage_list)
            
        else:
        # Use portland data
            location = 'Portland Oregon'
            coordinates_file = make_valid_filename(location + " coordinates")
            foliage_file = "Test_Data/Portland_Oregon_foliage.csv"
            foliage_list = parse_csv_file(foliage_file) #Name, Growth Rate, Average Lifespan
            treelist = TreeList(foliage_list)
            print(treelist.get_tree_names())
            print(treelist.get_all_tree_info())

    # Now to plot these trees on a graph of size (1,1)
    init_trees(foliage_file, coordinates_file)

    