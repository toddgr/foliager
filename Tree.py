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
    def __init__(self, species, x, y, age):
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
        self.species = species
        self.ba = (3.1415926 * species.b * species.b)/40000 # in meters squared, (A.64)
        self.c = 1. # competition index -> computed later
        self.bark_texture = species.bark_texture
        self.bark_color = species.bark_color
        self.leaf_shape = species.leaf_shape
        self.tree_form = species.tree_form

        self.position = (x,y)
        self.age = age # age of the tree in months

        # Assigned in create_forest/compute_dimensions():
        # self.height = self.generate_from(species.height)
        # self.dbh = self.generate_from(species.dbh)
        # self.lcl = self.generate_from(species.lcl)
        # self.c_diam = self.generate_from(species.c_diam)

        self.key = self.create_tree_key() # e.g. Ponderosa243123


    def generate_from(self, dimension):
        """
        Input: Some dimension from the species
        Output: A slightly randomized variation of that dimension for the tree
                using gaussian randomization
        """
        average = dimension
        stddev = (dimension + 0.05) / 4 # TODO make this var more accurate

        #new_dimension = Gaussian(average, stddev)
        #return abs(new_dimension) # dimension can't be negative
        # TODO testing without gauss dimension
        return round(dimension, 3)


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
        print(f'{self.species.deciduous_evergreen[0]}, about {round(self.age/12)} years old')
        print(f'position: {self.position}\nheight: {self.height} meters\ndbh: {self.dbh} meters ({round(self.dbh*100,3)} cm)')
        print(f'lcl: {self.lcl} meters\nc_diam: {self.c_diam} meters\n')
        pass


def generate_random_point(existing_points, parent_tree=None):
        """
        Ensures that there are no overlapping trees to start
        Makes sure they're evenly spaced
        """
        min_distance = 0.05
        max_tries = 100
        for _ in range(max_tries):
            if parent_tree:
                # tree should be generated within range of the parent tree
                max_distance = 0.2

                # Calculate initial range values
                x_low = parent_tree.position[0] - max_distance
                x_high = parent_tree.position[0] + max_distance
                z_low = parent_tree.position[1] - max_distance
                z_high = parent_tree.position[1] + max_distance

                # Clip values to be within [0, 1]
                x_low = max(0, x_low)
                x_high = min(1, x_high)
                z_low = max(0, z_low)
                z_high = min(1, z_high)

                x_random = np.random.rand()
                z_random = np.random.rand()

                # Scale and shift the values to the desired ranges
                x = x_low + (x_high - x_low) * x_random
                z = z_low + (z_high - z_low) * z_random

            else:
                x, z = np.random.rand(), np.random.rand()

            if all(distance.euclidean([x, z], p) >= min_distance for p in existing_points):
                return x, z

        return None, None


def plot_trees(forest:Forest, plot=False):

    coordinate_list = []
    # randomly create coordinates and assign a species to it
    for _ in range(forest.num_trees):
        x, y = generate_random_point(coordinate_list)
        x = round(x, 3)
        y = round(y, 3)
        species = np.random.choice(forest.species_list)  # Randomly choose a species name
        forest.add_tree(Tree(species, x, y, (forest.start_age * 12) + forest.t))
        coordinate_list.append([x, y])

    # =========== PLOT INITIAL TREES ========================
    if plot:
        # Create a colormap for the names
        unique_names = list(set(tree.name for tree in forest.trees_list))  # Get unique tree names
        colors = plt.cm.get_cmap('viridis', len(unique_names))  # Get a colormap with as many colors as names

        # Create a scatter plot
        for i, name in enumerate(unique_names):
            # Get the trees with the current name
            filtered_trees = [tree for tree in forest.trees_list if tree.name == name]
            
            # Plot these trees with a unique color
            plt.scatter([tree.position[0] for tree in filtered_trees], [tree.position[1] for tree in filtered_trees], 
                        label=name, color=colors(i))

        # Add labels, legend, and show the plot
        plt.title("Initial Tree Placement")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.show()
    # ==================================================================

    for month in range(forest.t):
        for tree in forest.trees_list:
            current_age = int((forest.start_age * 12) + month)# in months
            if month % 12 == 0: # trees can only spawn the last month of the year -- prevents spawning monthly 
                if current_age % (tree.species.masting_cycle * 12) == 0 and current_age >= int(tree.species.seeding_age * 12): # if the current age of the tree is
                    # create new tree position from current tree position
                    x, z = generate_random_point(coordinate_list, tree)
                    if x is not None:
                        coordinate_list.append([x,z])
                        # add to the forest
                        forest.add_tree(Tree(tree.species, x, z, (forest.t - month))) #TODO somehow add in the start age here too

    # =========== PLOT SPAWNED TREES TOO ========================
    if plot:
        # Create a colormap for the names
        unique_names = list(set(tree.name for tree in forest.trees_list))  # Get unique tree names
        colors = plt.cm.get_cmap('viridis', len(unique_names))  # Get a colormap with as many colors as names

        # Create a scatter plot
        for i, name in enumerate(unique_names):
            # Get the trees with the current name
            filtered_trees = [tree for tree in forest.trees_list if tree.name == name]
            
            # Plot these trees with a unique color
            plt.scatter([tree.position[0] for tree in filtered_trees], [tree.position[1] for tree in filtered_trees], 
                        label=name, color=colors(i))

        # Add labels, legend, and show the plot
        plt.title("Spawned Tree Placement")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.show()
    # ==================================================================

    return forest


if __name__ == '__main__':
    # Example usage:
    example_forest = Forest("test_data/prineville_oregon_climate.csv", "test_data/param_est_output.csv")
    plot_trees(example_forest, plot=True)
    example_forest.print_tree_list()