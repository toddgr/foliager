"""
File name: plot_trees.py
Author: Grace Todd
Date: September 16, 2024
Description: Initializes the coordinates for generated trees using scatter plot coordinates.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
from create_forest import Forest, Tree # TODO This is gonna cause problems I just know it

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