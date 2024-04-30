"""
File: param_estimator.py
Author: Grace Todd
Date: April 29, 2024
Description: A parameter estimation prototype for generating realistic 
            tree data for trees that aren't in the knowledge base
"""

from threepg_species_data import SpeciesData, parse_species_data

knowledge_base = "test_data/species_data_kb.csv"

def estimate_parameters(tree, knowledge_base):
    """ Uses the native habitat quality to estimate values for:
        df, kf, t_min, t_max, t_opt, kd, n_theta, c_theta 

        To start, we're just going to take the average for each of these values
        based on the similar trees in the KB

        Input: tree species to be estimated, knowledge base from which the values
        are estimated
        Output: tree with updated habitat values"""

    # Check if the tree is already in the knowledge base
    for kb_tree in knowledge_base:
        if tree.name == kb_tree.name:
            print(tree.name, " is already in the database.")
            return

    # Find similar habitats in the knowledge base
    similar_habitats = [kb_tree for kb_tree in knowledge_base if tree.q_habitat == kb_tree.q_habitat]
    
    print("Similar habitats for", tree.name, ":")
    for t in similar_habitats:
        print(t.name)

    # Find similar canopy density/leaf shape in the knowledge base
    # This is where the reward function would be really good; if a tree fulfills more than one of these, add a reward point
        # And then have a dictionary for them instead 
    similar_canopies = [kb_tree for kb_tree in knowledge_base if tree.q_canopy_density == kb_tree.q_canopy_density or \
                        tree.q_leaf_shape == kb_tree.q_leaf_shape or tree.q_deciduous_evergreen == kb_tree.q_deciduous_evergreen]

    print("\nSimilar leaves/canopies for", tree.name, ":")
    for t in similar_canopies:
        print(t.name)

    # Calculate average values for parameters
    # In the future, this will be replaced with a reward functionality
    parameter_count = len(similar_habitats)
    if parameter_count > 0:
        # Initialize parameter sums
        parameter_sums = [0] * 8  # Initialize with 8 parameters

        # Sum up parameter values
        for similar_tree in similar_habitats:
            for i in range(1, 9):  # Iterate through parameter values (from index 1 to 8)
                parameter_sums[i - 1] += float(getattr(similar_tree, ['df', 'kf', 't_min', 't_max', 't_opt', 'kd', 'n_theta', 'c_theta'][i - 1]))

        # Calculate average parameter values
        for i in range(1, 9):
            setattr(tree, ['df', 'kf', 't_min', 't_max', 't_opt', 'kd', 'n_theta', 'c_theta'][i - 1], parameter_sums[i - 1] / parameter_count)

def estimate_tree_list(tree_list, knowledge_base=None):
    """ Input: Knowledge Base, general information for a list of trees
        Output: Complete tree information for the list of trees """
    
    print("--- TREE LIST ---\n")
    for tree in tree_list:
        print(tree.name, ", ", tree.q_habitat)
        estimate_parameters(tree,knowledge_base)

    pass

if __name__ == "__main__":
    sample_tree = SpeciesData("Sessile Oak2","elliptical","dense","deciduous","green","oval","deep","temperate","furrows/ridges","gray/brown",4.3827,22.5405,35.9017,0,1,1.0739,0,0,0,9,0.7,0,0.433,0.035,0.0409,14.62,18.49,7.35,0.6,1,3,725,0.95,4,0.446,0.409,0.376,0,0,0,0.001,0,0,0,158.192,1.5916,0.5952,0.094,2.507,39.46,16.37,0,20.13,19.05,0,0.31,1.03,0,0.000031,2,1.05,0)
    kb = parse_species_data(knowledge_base)
    estimate_tree_list([sample_tree], kb)