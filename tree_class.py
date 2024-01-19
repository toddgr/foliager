"""
File: tree_class.py
Author: Grace Todd
Date: January 19, 2024
Description: Tree class. Holds information on a given tree type, derives information on each tree by parsing an input file.
            Currently only derives name, but will be able to hold more attributes in the future.
"""

class Tree:
    def __init__(self, name):
        self.name = name

def parse_tree_file(file_path):
    tree_list = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Split each line at the dot to extract the name
                parts = line.strip().split('. ')
                if len(parts) == 2:
                    name = parts[1]
                    print(name)
                    tree = Tree(name)
                    tree_list.append(tree)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return tree_list
