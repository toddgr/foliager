"""
File: param_estimator.py
Author: Grace Todd
Date: April 29, 2024
Description: A parameter estimation prototype for generating realistic 
            tree data for trees that aren't in the knowledge base
"""

from threepg_species_data import SpeciesData, parse_species_data

knowledge_base = "test_data/species_data_kb.csv"

def estimate_from_habitat(tree, knowledge_base):
    """ Uses the native habitat quality to estimate values for:
        df, kf, t_min, t_max, t_opt, kd, n_theta, c_theta 

        To start, we're jsut going to take the average for each of these values
        based on the similar trees in the KB

        Input: tree species to be estimated, knowledge base from which the values
        are estimated
        Output: tree with updated habitat values"""
    
    similar_habitats = []

    for kb_tree in knowledge_base:
        if tree.name == kb_tree.name:
            # this tree is already in the knowledge base-- we don't need to estimate
                tree.df = kb_tree.df
                tree.kf = kb_tree.kf
                tree.t_min = kb_tree.t_min
                tree.t_max = kb_tree.t_max
                tree.t_opt = kb_tree.t_opt
                tree.kd = kb_tree.kd
                tree.n_theta = kb_tree.n_theta
                tree.c_theta = kb_tree.c_theta

                print(tree.name, " is already in the database.")
                return
        
        if tree.q_habitat == kb_tree.q_habitat:
            similar_habitats.append(kb_tree)

    print("similar habitats for ", tree.name, ":")
    for t in similar_habitats:
        print(t.name)

    # for now, we'll just take the average for all of these. But in the future, we'll do a reward function
    tree.df = tree.kf = tree.t_min = tree.t_max = tree.t_opt = tree.kd = tree.n_theta = tree.c_theta = 0

    for similar_tree in similar_habitats:
        tree.df += similar_tree.df
        tree.kf += similar_tree.kf
        tree.t_min += similar_tree.t_min
        tree.t_max += similar_tree.t_max
        tree.t_opt += similar_tree.t_opt
        tree.kd += similar_tree.kd
        tree.n_theta += similar_tree.n_theta
        tree.c_theta += similar_tree.c_theta

    tree.df /= len(similar_habitats)
    tree.kf /= len(similar_habitats)
    tree.t_min /= len(similar_habitats)
    tree.t_max /= len(similar_habitats)
    tree.t_opt /= len(similar_habitats)
    tree.kd /= len(similar_habitats)
    tree.n_theta /= len(similar_habitats)
    tree.c_theta /= len(similar_habitats)

    print("tree info:", tree.df,tree.kf,tree.t_min,tree.t_max,tree.t_opt,tree.kd,tree.n_theta,tree.c_theta)
    pass

def param_est(tree_list, knowledge_base=None):
    """ Input: Knowledge Base, general information for a list of trees
        Output: Complete tree information for the list of trees """
    
    print("--- TREE LIST ---\n")
    for tree in tree_list:
        print(tree.name, ", ", tree.q_habitat)
        estimate_from_habitat(tree,knowledge_base)

    pass

if __name__ == "__main__":
    sample_tree = SpeciesData("Sessile Oak2","elliptical","dense","deciduous","green","oval","deep","temperate","furrows/ridges","gray/brown",4.3827,22.5405,35.9017,None,1,1.0739,None,None,None,9,0.7,None,0.433,0.035,0.0409,14.62,18.49,7.35,0.6,1,3,725,0.95,4,0.446,0.409,0.376,0,0,0,0.001,None,None,0,158.192,1.5916,0.5952,0.094,2.507,39.46,16.37,0,20.13,19.05,0,0.31,1.03,0,0.000031,2,1.05,0)
    kb = parse_species_data(knowledge_base)
    param_est([sample_tree], kb)