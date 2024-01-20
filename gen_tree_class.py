"""
File: gen_tree_class.py
Author: Grace Todd
Date: January 19, 2024
Description: Generates tree class and ensures that the tree class updates with new attributes provided in default_tree_chart.csv.
            Takes in the attributes from default_tree_chart, ensures that the tree class has the correct attributes and 
            corresponding functions. If not, modifies tree_class
"""

from datetime import datetime
from parse_tree_input import csv_file_to_list

tree_class_file_name = "tree_class_test.py"
default_tree_chart = "default_tree_chart.csv"

def create_header():
    file_name = 'File name: ' + tree_class_file_name + '\n'
    author = 'Author: Grace Todd\n'
    # Get today's date
    current_date = datetime.now().date()
    # Format the date as a string
    date_string = current_date.strftime("%B %d, %Y")
    todays_date = "Date: " + date_string + "\n"
    description = "Description: " + "Tree class. Holds information on a given tree type, derives information on each tree by parsing an input file.\n"
    
    header = '\"\"\"\n' + file_name + author + todays_date + description + '\"\"\"\n'
    return header

def get_attributes_from_csv(file_name):
    attributes = csv_file_to_list(file_name)
    attributes = [element for sublist in attributes for element in sublist]
    attributes = [s.lower() for s in attributes]
    attributes = [s.replace(' ', '_') for s in attributes]
    return attributes

def create_function_definition(function_title, parameters=None):
    return "def " + function_title + "(" + parameters + "):\n"

def create_tree_constructor():
    # for each attribute in the CSV file, create a Tree attribute
    attributes_list = get_attributes_from_csv(default_tree_chart)
    parameters = "self"
    assignments = ""
    for attribute in attributes_list:
        parameters = parameters + ", " + attribute
        assignments += "\t\tself." + attribute + " = " + attribute + "\n"

    definition = "\t" + create_function_definition("__init__", parameters)
    
    return definition + assignments

def create_get_functions():
    attributes_list = get_attributes_from_csv(default_tree_chart)
    get_functions = ""
    for attribute in attributes_list:
        get_functions += "\n\t" + create_function_definition("get_" + attribute, "self")
        get_functions += "\t\treturn self." + attribute + "\n"

    return get_functions

def create_tree_class():
    definition = "class Tree:\n\n"
    #create_init with attributes from csv
    init = create_tree_constructor()
    #create get functions for all attributes from csv
    get_functions = create_get_functions()
    return definition + init + get_functions

def create_tree_list_class():
    pass

def write_file():
    header = create_header()
    tree_class = create_tree_class()
    return header + tree_class

if __name__ == '__main__':
    attributes_list = get_attributes_from_csv(default_tree_chart)
    print("Attributes:", attributes_list)

    with open(tree_class_file_name, 'w') as file:
        # Create header
        file.write(
            write_file()
        )

