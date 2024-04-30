"""
File: param_estimator.py
Author: Grace Todd
Date: April 29, 2024
Description: A parameter estimation prototype for generating realistic 
            tree data for trees that aren't in the knowledge base
"""

from threepg_species_data import SpeciesData, parse_species_data

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

        # root attributes

        # habitat attributes

        # Check if the tree has earned any points
        if points > 0:
            points_dict[kb_tree] = points

    return points_dict

def calculate_parameter_values(tree, point_dict):
    """ This function will take into account the different point values assigned to each kb tree, and 
        use those point values to calculate/estimate the values for each of the tree parameters.
        
        Different attributes will be influenced by different similarities"""
    pass


def estimate_parameters(tree, knowledge_base):
    """ Uses the common knowledge qualities of a tree to estimate scientific values

        To start, we're just going to take the average for each of these values
        based on the similar trees in the KB

        Input: tree species to be estimated, knowledge base from which the values
        are estimated
        Output: tree species with updated habitat values"""

    # Check if the tree is already in the knowledge base
    for kb_tree in knowledge_base:
        if tree.name == kb_tree.name:
            print(tree.name, " is already in the database.")
            return

    #------ CHECK THE KNOWLEDGE BASE FOR SIMILARITIES -----
    # Find similar habitats in the knowledge base
    similar_habitats = [kb_tree for kb_tree in knowledge_base if tree.q_habitat == kb_tree.q_habitat]
    
    print("Similar habitats for", tree.name, ":")
    for t in similar_habitats:
        print(t.name)

    # Find similar canopy density/leaf shape in the knowledge base
    # This is where the reward function would be really good; if a tree fulfills more than one of these, add a reward point
        # And then have a dictionary for them instead 
    similar_canopies = find_similarities(tree, knowledge_base)
    
    print(f"\nSimilar leaves/canopies for {tree.name}:")
    # Print tree name and corresponding point value
    for tree, points in similar_canopies.items():
        print(f"{tree.name}: {points}")


    # ------ CALCULATE THE PARAMETER VALUES -------
    # Calculate average values for parameters
    # In the future, this will be replaced with a reward functionality
    habitats_count = len(similar_habitats)
    if habitats_count > 0:
        # Initialize parameter sums
        parameter_sums = [0] * 8  # Initialize with 8 parameters

        # Sum up parameter values
        for similar_tree in similar_habitats:
            for i in range(8):  # Iterate through parameter values (from index 1 to 8)
                parameter_sums[i] += float(getattr(similar_tree, ['df', 'kf', 't_min', 't_max', 't_opt', 'kd', 'n_theta', 'c_theta'][i]))

        # Calculate average parameter values
        for i in range(8):
            setattr(tree, ['df', 'kf', 't_min', 't_max', 't_opt', 'kd', 'n_theta', 'c_theta'][i], parameter_sums[i] / habitats_count)


def estimate_tree_list(tree_list, knowledge_base=None):
    """ Input: Knowledge Base, general information for a list of trees
        Output: Complete tree information for the list of trees """
    
    print("--- TREE LIST ---\n")
    for tree in tree_list:
        #print(tree.name, ", ", tree.q_habitat)
        estimate_parameters(tree,knowledge_base)

    pass

# Example usage
if __name__ == "__main__":
    # Define a sample tree. All of these values are common knowledge and can be determined by the nlp
    sample_tree = SpeciesData("Imaginary Tree","elliptical","dense","deciduous","green","oval","deep","temperate","furrows/ridges","gray/brown")
    kb = parse_species_data(knowledge_base_filepath)
    estimate_tree_list([sample_tree], kb)