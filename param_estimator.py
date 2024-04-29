"""
File: param_estimator.py
Author: Grace Todd
Date: April 29, 2024
Description: A parameter estimation prototype for generating realistic 
            tree data for trees that aren't in the knowledge base
"""

from threepg_species_data import SpeciesData, parse_species_data

knowledge_base = "test_data/species_data_kb.csv"

def param_est(tree_list, knowledge_base=None):
    """ Input: Knowledge Base, general information for a list of trees
        Output: Complete tree information for the list of trees """
    
    print("--- TREE LIST ---\n")
    for tree in tree_list:
        print(tree.name)

    pass

if __name__ == "__main__":
    kb = parse_species_data(knowledge_base)
    param_est(kb)