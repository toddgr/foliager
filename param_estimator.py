"""
File: param_estimator.py
Author: Grace Todd
Date: April 29, 2024
Description: A parameter estimation prototype for generating realistic 
            tree data for trees that aren't in the knowledge base
"""

from threepg_species_data import SpeciesData, parse_species_data, csv_file_to_list
import csv

knowledge_base_filepath = "test_data/species_data_kb.csv"

def find_similarities(tree, knowledge_base):
    """ A rudimentary point-assigning system for determining which trees will have the 
        most algorithmic influence
        
        i.e. the more conditions a tree fulfills, the more influence it will have
        
        Go through all of the trees in the knowledge base, find what is common, 
        and then later on in the code we can parse through this to determine
        which points and trees will have the greatest effect over which aspects?

        Or maybe it would be better to calculate a score for each category and work from there?
        Things to think about 
        
        For now, or maybe forever, we only compare attributes that are equal to
        that of the current tree... not those that are almost equal.
        (i.e. if a kb tree has a "very thin" canopy and the estimated tree is "thin",
        the code does not consider the kb tree. For that attribute, at least.)
        """

    points_dict = {}  # Dictionary to store tree and corresponding points

    for kb_tree in knowledge_base:
        points = 0  # Initialize points for current tree

        # leaf attributes
        if tree.q_canopy_density == kb_tree.q_canopy_density:
            points += 1

        if tree.q_leaf_shape == kb_tree.q_leaf_shape:
            points += 1

        if tree.q_deciduous_evergreen == kb_tree.q_deciduous_evergreen:
            points += 1

        # to be used when more leaf colors than "green"
        #if tree.q_leaf_color == kb_tree.q_leaf_color:
            #points +=1

        # might need to change this --- compares items in a list to items in a list
        if tree.q_tree_form == kb_tree.q_tree_form:
            points += 1

        # root attributes
        if tree.q_tree_roots == kb_tree.q_tree_roots:
            points += 1        

        # habitat attributes
        # might need to change this --- compares items in a list to items in a list
        if tree.q_habitat == kb_tree.q_habitat:
            points += 1

        # bark attributes
        if tree.q_bark_texture == kb_tree.q_bark_texture:
            points += 1

        if tree.q_bark_color == kb_tree.q_bark_color:
            points += 1

        # Check if the tree has earned any points
        if points > 0:
            points_dict[kb_tree] = points

    return points_dict

def calculate_parameter_values(tree, point_dict):
    """ This function will take into account the different point values assigned to each kb tree, and 
        use those point values to calculate/estimate the values for each of the tree parameters.
        
        Different attributes will be influenced by different similarities
        Leaf similarity:
        k, acx, sla_1, sla_0, t_sla_mid,yfx, yf0, tyf

        Canopy similarity:
        tc, mf, p2, p20, ms, wsx1000, nm, mf

        Root/wood/bark similarity:
        mr, ms, yr, nr_min, nr_max, m_0, ah,nhb, nhc, ahl, nhlb, nhlc, ak, nkb, nkh, av, nvb, nvh, nvbh

        Habitat similarity:
        t_min, t_opt, t_max, kd, n_theta, c_theta

        General similarity:
        fcax_700, fn0, nfn, r_age, n_age, max_age
        """

    # for now, I'm just going to assign the exact parameters for the most similar tree
    # I'll reconfigure later

    most_similar_tree = max(point_dict, key=point_dict.get)
    tree = calculate_leaf_similarity(tree, most_similar_tree)
    tree = calculate_canopy_similarity(tree, most_similar_tree)
    tree = calculate_wood_similarity(tree, most_similar_tree)
    tree = calculate_habitat_similarity(tree, most_similar_tree)
    tree = calculate_general_similarity(tree, most_similar_tree)
    
    return tree


def calculate_leaf_similarity(tree, kb_tree):
    """ Calculate the parameters associated with similar leaf styles
        k, acx, sla_1, sla_0, t_sla_mid,yfx, yf0, tyf
    """
    tree.k = kb_tree.k
    tree.acx = kb_tree.acx
    tree.sla_1 = kb_tree.sla_1
    tree.sla_0 = kb_tree.sla_0
    tree.t_sla_mid = kb_tree.t_sla_mid
    tree.yfx = kb_tree.yfx
    tree.yf0 = kb_tree.yf0
    tree.tyf = kb_tree.tyf
    
    return tree


def calculate_canopy_similarity(tree, kb_tree):
    """ Calculate the parameters associated with similar canopy styles
        tc, mf, p2, p20, ms, wsx1000, nm, mf
    """
    tree.tc = kb_tree.tc
    tree.mf = kb_tree.mf
    tree.p2 = kb_tree.p2
    tree.p20 = kb_tree.p20
    tree.wsx1000 = kb_tree.wsx1000
    tree.nm = kb_tree.nm
    tree.kf = kb_tree.kf

    return tree


def calculate_wood_similarity(tree, kb_tree):
    """ Calculate the parameters associated with similar wood styles
    mr, ms, yr, nr_min, nr_max, m_0, ah,nhb, nhc, ahl, nhlb, nhlc, 
    ak, nkb, nkh, av, nvb, nvh, nvbh
    """
    tree.mr = kb_tree.mr
    tree.ms = kb_tree.ms
    tree.yr = kb_tree.yr
    tree.nr_min = kb_tree.nr_min
    tree.nr_max = kb_tree.nr_max
    tree.m_0 = kb_tree.m_0
    tree.nhb = kb_tree.nhb
    tree.nhc = kb_tree.nhc
    tree.ahl = kb_tree.ahl
    tree.nhlb = kb_tree.nhlb
    tree.nhlc = kb_tree.nhlc
    tree.ak = kb_tree.ak
    tree.nkb = kb_tree.nkb
    tree.nkh = kb_tree.nkh
    tree.av = kb_tree.av
    tree.nvb = kb_tree.nvb
    tree.nvh = kb_tree.nvh
    tree.nvbh = kb_tree.nvbh

    return tree


def calculate_habitat_similarity(tree, kb_tree):
    """ Calculate the parameters associates with similar habitats
    t_min, t_opt, t_max, kd, n_theta, c_theta
    """
    tree.t_opt = kb_tree.t_opt
    tree.t_min = kb_tree.t_min
    tree.t_max = kb_tree.t_max
    tree.kd = kb_tree.kd
    tree.n_theta = kb_tree.n_theta
    tree.c_theta = kb_tree.c_theta
    tree.aws = kb_tree.aws
    tree.nws = kb_tree.nws

    return tree


def calculate_general_similarity(tree, kb_tree):
    """ Calculate the parameters associated with general similarities
    fcax_700, fn0, nfn, r_age, n_age, max_age
    """
    tree.fcax_700 = kb_tree.fcax_700
    tree.fn0 = kb_tree.fn0
    tree.nfn = kb_tree.nfn
    tree.r_age = kb_tree.r_age
    tree.n_age = kb_tree.n_age
    tree.max_age = kb_tree.max_age

    return tree


def estimate_parameters(tree, knowledge_base):
    """ Uses the common knowledge qualities of a tree to estimate scientific values

        To start, we're just going to take the average for each of these values
        based on the similar trees in the KB

        Input: tree species to be estimated, knowledge base from which the values
        are estimated
        Output: tree species with updated habitat values"""

    knowledge_base = parse_species_data(knowledge_base)
    # Check if the tree is already in the knowledge base
    for kb_tree in knowledge_base:
        if tree.name == kb_tree.name:
            print(f"\n{tree.name} is already in the database.")
            return kb_tree.get_species_info()

    #------ CHECK THE KNOWLEDGE BASE FOR SIMILARITIES -----
    # Find similar habitats in the knowledge base
    similar_habitats = [kb_tree for kb_tree in knowledge_base if tree.q_habitat == kb_tree.q_habitat]
    
    # print("Similar habitats for", tree.name, ":")
    # for t in similar_habitats:
    #     print(t.name)

    # Find similar canopy density/leaf shape in the knowledge base
    # This is where the reward function would be really good; if a tree fulfills more than one of these, add a reward point
        # And then have a dictionary for them instead 
    similar_trees = find_similarities(tree, knowledge_base)
    complete_tree = calculate_parameter_values(tree, similar_trees)
    
    # print(f"\nSimilar leaves/canopies for {tree.name}:")
    # # Print tree name and corresponding point value
    # for tree, points in similar_trees.items():
    #     print(f"{tree.name}: {points}")

    # print("\n\n")
    #complete_tree.print_species_data()
    # print(complete_tree.get_species_info())
    return complete_tree.get_species_info()


def estimate_tree_list(tree_list, knowledge_base, io_filepath):
    """ Input: Knowledge Base, general information for a list of trees
        Output: Complete tree information for the list of trees """
    with open(io_filepath, 'w') as file:
        file.write("# name,name_scientific,q_leaf_shape,q_canopy_density,d_deciduous_evergreen,q_leaf_color,q_tree_form,q_tree_roots,q_habitat,q_bark_texture,q_bark_color,t_min,t_opt,t_max,kf,fcax_700,kd,n_theta,c_theta,p2,p20,acx,sla_1,sla_0,t_sla_mid,fn0,nfn,tc,max_age,r_age,n_age,mf,mr,ms,yfx,yf0,tyf,yr,nr_max,nr_min,m_0,wsx1000,nm,k,aws,nws,ah,nhb,nhc,ahl,nhlb,nhlc,ak,nkb,nkh,av,nvb,nvh,nvbh\n")
        for tree in tree_list:
            # print(tree.name, ", ", tree.q_habitat)
            tree_info = estimate_parameters(tree, knowledge_base)
            file.write(tree_info)
            file.write("\n")
            

# Example usage
if __name__ == "__main__":
    # Define a sample tree. All of these values are common knowledge and can be determined by the nlp
    io_file = "douglas_fir_coordinates_foliage.csv"
    sample_tree = SpeciesData("Imaginary Tree","T. Madeupicus","elliptical","dense","deciduous","green","oval","deep","temperate","furrows/ridges","gray/brown")
    #kb = parse_species_data(knowledge_base_filepath)
    estimate_tree_list([sample_tree], knowledge_base_filepath, io_file)