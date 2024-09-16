"""
File name: plot_trees.py
Author: Grace Todd
Date: September 16, 2024
Description: Initializes the coordinates for generated trees using scatter plot coordinates.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

from gauss import Gaussian
from Forest import Forest

class Tree():
    """
    Holds information about each individual tree in the forest.
    Inherits information about its species
    Calculates unique dimensions on initialization
    Initialization occurs when the (x,y) coordinates are generated
    TODO break up into two classes, Qualities and dimensions?
    """
    def __init__(self, species, x, y):
        """
        Attributes:
            Inherited
            - name
            - bark_texture
            - bark_color
            - leaf_shape
            - tree_form
            Calculated
            - position (x, y) -> from coordinate generator
            - height -> from species, with randomization
            - dbh
            - lcl
            - c_diam
        """
        self.name = species.name
        self.bark_texture = species.bark_texture
        self.bark_color = species.bark_color
        self.leaf_shape = species.leaf_shape
        self.tree_form = species.tree_form

        self.position = (x,y)
        self.height = self.generate_from(species.height)
        self.dbh = self.generate_from(species.dbh)
        self.lcl = self.generate_from(species.lcl)
        self.c_diam = self.generate_from(species.c_diam)

        self.key = self.create_tree_key() # e.g. Ponderosa243123


    def generate_from(self, dimension):
        """
        Input: Some dimension from the species
        Output: A slightly randomized variation of that dimension for the tree
                using gaussian randomization
        """
        average = dimension
        stddev = (dimension + 0.005) / 4 # TODO make this var more accurate

        new_dimension = Gaussian(average, stddev)
        return abs(new_dimension) # dimension can't be negative


    def create_tree_key(self):
        """
        Input: Unique position of the tree
        Output: A string that will uniquely represent the tree.
                First word of the species name + x + y
                i.e. Ponderosa184339
        """

        name = self.name.split()[0] # First word of the species name
        x = str(int(self.position[0] * 1000)) # ex. 0.183444 -> '183'
        y = str(int(self.position[1] * 1000)) # ex. 0.234950 -> '234'

        return name + x + y


    def get_tree_info(self):
        """
        Prints basic information about a tree's dimensions.
        """
        print(f'========== {self.key} ==========')
        print(f'position: {self.position}\nheight: {self.height}\ndbh: {self.dbh}')
        print(f'lcl: {self.lcl}\nc_diam: {self.c_diam}\n')

def plot_trees(forest:Forest, plot=False, num_trees=50, min_distance=0.05):
    """
    Input: Forest class object
    Output: Forest, but with a populated tree list using tree class objects
    Used for initial placement of trees
    """
    
    def generate_random_point(existing_points, min_distance):
        """
        Ensures that there are no overlapping trees to start
        Makes sure they're evenly spaced
        """
        while True:
            x, z = np.random.rand(), np.random.rand()
            if all(distance.euclidean([x, z], p) >= min_distance for p in existing_points):
                return x, z

    np.random.seed(np.random.randint(0,100))
    points = []
    
    # Generate the random coordinates
    for _ in range(num_trees):
        x, z = generate_random_point(points, min_distance)
        points.append([x, z])
    
    x_values, z_values = np.array(points).T  # Split the points into x and z coordinates

    tree_names = [species.name for species in forest.species_list] # Get species names from the forest
    
    tree_name = np.random.choice(tree_names, num_trees)  # Randomly select tree names

    # Sort tree_name and corresponding x_values and z_values by tree_name
    sorted_indices = np.argsort(tree_name)
    tree_name = tree_name[sorted_indices]
    x_values = x_values[sorted_indices]
    z_values = z_values[sorted_indices]

    # ============ PLOTTING STUFF ===============
    # Used mostly for debug
    if plot:
        label_colors = {label: plt.colormaps.get_cmap('viridis')(i / len(tree_names)) for i, label in enumerate(tree_names)}

        for label, color in label_colors.items():
            plt.scatter(x_values[tree_name == label], z_values[tree_name == label], label=label, color=color)

        plt.title('Initial Tree Placement')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
    # ===========================================

    # Create tree class objects out of the positions and tree names
    for i in range(num_trees):
        for species in forest.species_list:
            if species.name == tree_name[i]:
                forest.add_tree(Tree(species, x_values[i], z_values[i]))
                continue
    
    return forest


if __name__ == '__main__':
    # Example usage:
    example_forest = Forest("test_data/prineville_oregon_climate.csv", "test_data/param_est_output.csv")
    plot_trees(example_forest, plot=True, num_trees=100)
    example_forest.print_tree_list()