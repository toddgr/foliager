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
        parameters = parameters + ", " + attribute + "=None"
        assignments += "\t\tself." + attribute + " = " + attribute + "\n"

    definition = "\t" + create_function_definition("__init__", parameters)
    
    return definition + assignments

def create_tree_get_functions():
    attributes_list = get_attributes_from_csv(default_tree_chart)
    get_functions = ""
    get_all_function = "\n\t" + create_function_definition("get_tree_info", "self") + "\t\treturn "
    for attribute in attributes_list:
        get_functions += "\n\t" + create_function_definition("get_" + attribute, "self")
        get_functions += "\t\treturn self." + attribute + "\n"
        get_all_function += "self." + attribute + ", "

    get_functions += get_all_function + "\n"

    return get_functions

def create_tree_class():
    definition = "\n\nclass Tree:\n\n"
    #create_init with attributes from csv
    init = create_tree_constructor()
    #create get functions for all attributes from csv
    get_functions = create_tree_get_functions()
    return definition + init + get_functions

def create_tree_list_get_functions():
    attributes_list = get_attributes_from_csv(default_tree_chart)
    get_functions = ""
    get_all_function = "\n\t" + create_function_definition("get_all_tree_info", "self") + "\t\treturn [tree.get_tree_info() for tree in self.trees]"
    for i, attribute in enumerate(attributes_list):
        get_functions += "\n\t" + create_function_definition("get_tree_" + attribute + "s", "self")
        if i== 0:
            get_functions += "\t\treturn [[tree.get_" + attribute + "()] for tree in self.trees]\n"
        else:
            get_functions += "\t\treturn [[tree.get_tree_" + attributes_list[0] + "(), tree.get_" + attribute + "()] for tree in self.trees]\n"

    return get_functions + get_all_function

def create_tree_list_class():
    definition = "\nclass TreeList:\n\n"
    #create init
    init = "\tdef __init__(self, tree_list=None):\n\
\t\tif tree_list is not None:\n\
\t\t\tself.trees = tree_list\n\
\t\telse:\n\
\t\t\tself.trees = []\n\n"

    add_tree = "\tdef add_trees(self, tree):\n\
\t\tself.trees.append(tree)\n"

    get_functions = create_tree_list_get_functions()

    return definition + init + add_tree + get_functions

def write_file():
    header = create_header()
    tree_class = create_tree_class()
    tree_list_class = create_tree_list_class()
    return header + tree_class + tree_list_class

if __name__ == '__main__':
    attributes_list = get_attributes_from_csv(default_tree_chart)
    print("Attributes:", attributes_list)

    with open(tree_class_file_name, 'w') as file:
        file.write(
            write_file()
        )

