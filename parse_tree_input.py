"""
File: parse_tree_input.py
Author: Grace Todd
Date: January 19, 2024
Description: Parses text files into Python objects Tree and TreeList, which will hold information about specific tree types.
"""

from tree_class import Tree, TreeList

def parse_tree_file(file_path):
    tree_list = TreeList()

    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Split each line at the dot to extract the name
                parts = line.strip().split('. ')
                if len(parts) == 2:
                    name = parts[1]
                    tree = Tree(name)
                    tree_list.add_tree(tree)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return tree_list