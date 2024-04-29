"""
File: param_estimator.py
Author: Grace Todd
Date: April 29, 2024
Description: A parameter estimation prototype for generating realistic 
            tree data for trees that aren't in the knowledge base
"""

from threepg_species_data import SpeciesData

knowledge_base = "test_data/species_data_kb.csv"

def param_est(tree_list, knowledge_base=None):
    """ Input: Knowledge Base, general information for a list of trees
        Output: Complete tree information for the list of trees """
    
    print("--- TREE LIST ---\n")
    for tree in tree_list:
        print(tree.name)

    pass

if __name__ == "__main__":
    sample_tree = SpeciesData("Swiss Pine",1.0418,22.97,35.5482,None,1,1.196,None,None,None,9,0.7,None,\
                              1.1724,0.2141,0.0285,4.6,4.6,1,0.6,1,3,900,0.95,4,0.606,0.573,0.571,0.0024,\
                              0.001,60,0.001,None,None,0,177.331,1.7806,0.389,0.128,2.305,43.7,29.1,0,18.07,\
                            26.58,0,0.62,0.7,0,0.00021,2.15,0.29,0, None, None, None, None, None, None, None, None, None)
    param_est(tree_list=[sample_tree])