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

def create_header():
    file_name = 'File name: tree_class_test.py\n'
    author = 'Author: Grace Todd\n'
    # Get today's date
    current_date = datetime.now().date()
    # Format the date as a string
    date_string = current_date.strftime("%Y-%m-%d")
    todays_date = "Date: " + date_string + "\n"
    description = "Tree class. Holds information on a given tree type, derives information on each tree by parsing an input file.\n\
            Currently only derives name, but will be able to hold more attributes in the future.\n"
    
    header = '\"\"\"\n' + file_name + author + todays_date + description + '\"\"\"\n'
    return header

def get_attributes_from_csv(file_name):
    attributes = csv_file_to_list(file_name)
    attributes = [element for sublist in attributes for element in sublist]
    attributes = [s.lower() for s in attributes]
    attributes = [s.replace(' ', '_') for s in attributes]
    return attributes


def create_tree_class():
    definition = "class Tree():\n"
    #create_init with attributes from csv
    #create get functions for all attributes from csv

    pass

def create_tree_list_class():
    pass

if __name__ == '__main__':
    attributes_list = get_attributes_from_csv('default_tree_chart.csv')
    print("Attributes:", attributes_list)
    
    with open(tree_class_file_name, 'w') as file:
        # Create header
        file.write(
            create_header()
        )

