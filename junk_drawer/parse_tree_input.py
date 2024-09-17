"""
File: parse_tree_input.py
Author: Grace Todd
Date: January 19, 2024
Description: Parses text files into Python objects Tree and TreeList, which will hold information about specific tree types.
"""


import csv

# def parse_tree_file(file_path):
#     tree_list = TreeList()

#     try:
#         with open(file_path, 'r') as file:
#             for line in file:
#                 # Split each line at the dot to extract the name
#                 parts = line.strip().split('. ')
#                 if len(parts) == 2:
#                     name = parts[1]
#                     tree = Tree(name)
#                     tree_list.add_tree(tree)

#     except FileNotFoundError:
#         print(f"File not found: {file_path}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

#     return tree_list


def csv_file_to_string(file_path):
    # Reads in the default_tree_chart.csv headers and converts them to a 
    # usable string for the NLP prompt
    result_string = ""

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Exclude lines starting with a comment character (e.g., #)
            if not row or row[0].startswith("#"):
                continue
            result_string += ','.join(row) + '\n'

    return result_string


def csv_file_to_float_list(file_path):
    # specifically for reading CSVs that contain floats, not strings
    attribute_list = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Exclude lines starting with a comment character (e.g., #)
            if not row or row[0].startswith("#"):
                continue

            # Convert all elements in the row to float, excluding the first one (first element is species name, string)
            data_row = [row[0]] + [float(element) for element in row[1:]]
            attribute_list.append(data_row)
    return attribute_list

def csv_file_to_list(file_path):
    attribute_list = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Exclude lines starting with a comment character (e.g., #)
            if not row or row[0].startswith("#"):
                continue
            attribute_list.append(row)
    return attribute_list