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
    def __init__(self, species, x, y, age=0):
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
        self.ba = (np.pi * species.b * species.b)/40000 # TODO should b be species specific?
        self.c = 1. # competition index -> computed later
        self.bark_texture = species.bark_texture
        self.bark_color = species.bark_color
        self.leaf_shape = species.leaf_shape
        self.tree_form = species.tree_form

        self.position = (x,y)
        self.age = age
        #self.compute_dimensions()
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
    
    # Generate the random initial coordinates
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


def generate_random_point(existing_points, parent_tree=None):
        """
        Ensures that there are no overlapping trees to start
        Makes sure they're evenly spaced
        """
        min_distance = 0.05
        max_tries = 100
        for _ in range(max_tries):
            if parent_tree:
                print("Trying to fit a tree here ...")
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
            else:
                print("trying again")
            
        print("We can't fit a tree here! Cancelling ...")
        return None, None


def plot_trees_differently(forest:Forest, plot=False):

    coordinate_list = []
    # randomly create coordinates and assign a species to it
    for _ in range(forest.num_trees):
        x, y = generate_random_point(coordinate_list)
        species = np.random.choice(forest.species_list)  # Randomly choose a species name
        forest.add_tree(Tree(species, x, y, forest.t))
        coordinate_list.append([x, y])

    # =========== PLOT INITIAL TREES ========================
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

    MASTING_CYCLE = 2

    for month in range(forest.t):
        print(f'MONTH {month}/{forest.t}')
        for tree in forest.trees_list:
            print(f'Tree: {tree.name}, {tree.position}')
            current_age = (tree.age - forest.t) + month + 1 # current age of the tree in the simulation
            print(f'current_age: {current_age}')
            if current_age % MASTING_CYCLE == 0: # if the current age of the tree is
                # create new tree position from current tree position
                print("===== masting time =====")
                x, z = generate_random_point(coordinate_list, tree)
                if x is not None:
                    coordinate_list.append([x,z])
                    # add to the forest
                    forest.add_tree(Tree(tree.species, x, z, forest.t-month))

    # =========== PLOT SPAWNED TREES TOO ========================
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
    pass


if __name__ == '__main__':
    # Example usage:
    example_forest = Forest("test_data/prineville_oregon_climate.csv", "test_data/param_est_output.csv")
    #plot_trees_with_spawning(example_forest, plot=True, num_trees=1)
    plot_trees_differently(example_forest, plot=True)
    example_forest.print_tree_list()