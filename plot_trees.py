"""
File name: plot_trees.py
Author: Grace Todd
Date: September 16, 2024
Description: Initializes the coordinates for generated trees using scatter plot coordinates.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
from create_forest import Forest # This is gonna cause problems I just know it

def plot_trees(forest:Forest, plot=False, num_trees=50, min_distance=0.05):
    """
    Takes in a tree_chart csv, outputs a series of random tree placements to a CSV (name,x,y)
    Can use 3pg, can create a scatter plot visualization
    Used for initial placement of trees to apply 3PG
    NEW VERSION SORTS THE ENTRIES SO THAT THEY ARE GROUPED BY TREE NAME
    """
    
    def generate_random_point(existing_points, min_distance):
        while True:
            x, z = np.random.rand(), np.random.rand()
            if all(distance.euclidean([x, z], p) >= min_distance for p in existing_points):
                return x, z

    np.random.seed(np.random.randint(0,100))
    points = []
    
    for _ in range(num_trees):
        x, z = generate_random_point(points, min_distance)
        points.append([x, z])
    
    x_values, z_values = np.array(points).T  # Split the points into x and z coordinates

    tree_names = [species.name for species in forest.species_list]
    
    tree_name = np.random.choice(tree_names, num_trees)  # Randomly select tree names

    # Sort tree_name and corresponding x_values and z_values by tree_name
    sorted_indices = np.argsort(tree_name)
    tree_name = tree_name[sorted_indices]
    x_values = x_values[sorted_indices]
    z_values = z_values[sorted_indices]

    # ============ PLOTTING STUFF ===============
    if plot:
        label_colors = {label: plt.colormaps.get_cmap('viridis')(i / len(tree_names)) for i, label in enumerate(tree_names)}

        for label, color in label_colors.items():
            plt.scatter(x_values[tree_name == label], z_values[tree_name == label], label=label, color=color)

        plt.title('Initial Tree Placement')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

    # Prepare rows for output
    rows = [['name', 'x', 'z']]
    for x, z, label in zip(x_values, z_values, tree_name):
        rows.append([label, x, z])

    return rows

# Example usage:
example_forest = Forest("test_data/prineville_oregon_climate.csv", "test_data/param_est_output.csv")
plot_trees(example_forest, plot=True, num_trees = 100)