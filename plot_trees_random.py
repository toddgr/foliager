"""
File name: plot_trees_random.py
Author: Grace Todd
Date: February 22, 2024
Description: Initializes the coordinates for generated trees using scatter plot coordinates.
"""

import numpy as np
import csv
import matplotlib.pyplot as plt
from junk_drawer.tree_class import TreeList
from parse_csv_file import parse_csv_file
from threepg_species_data import SpeciesData, get_tree_names, parse_species_data

def init_trees(foliage_file, output_csv_file, threepg=True, plot=False):
    """
        Takes in a tree_chart csv, outputs a series of random tree placements to a CSV (name,x,y)
        Can use 3pg, can create a scatter plot visualization
        Used for initial placement of trees to apply 3PG
    """
    # Generate random data for the x and z coordinates
    np.random.seed(42)
    num_trees = 50
    x_values = np.random.rand(num_trees)
    z_values = np.random.rand(num_trees)
    if threepg: 
        # use species data instead of Treelist. TODO make these the same class
        treelist = parse_species_data(foliage_file)
        tree_names = get_tree_names(treelist)
    else:
        treelist = TreeList(parse_csv_file(foliage_file))
        tree_names = treelist.get_tree_names()
    tree_name = np.random.choice(tree_names, num_trees)  # Randomly select tree names

    # ============ PLOTTING STUFF ===============
    if plot:
        # Define colors for each label
        label_colors = {label: plt.colormaps.get_cmap('viridis')(i / len(tree_names)) for i, label in enumerate(tree_names)}

        # Create a scatter plot with colored points
        for label, color in label_colors.items():
            plt.scatter(x_values[tree_name == label], z_values[tree_name == label], label=label, color=color)

        # Add labels and title
        plt.title('Initial Tree Placement')

        # Add legend
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()  # Adjust layout to prevent clipping

        # Save the plot to a file (optional)
        #plt.savefig('initial_tree_placement.png')

    # Write x, y, and label data to CSV file
    with open(output_csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['name', 'x', 'z'])  # Write header
        for x, z, label in zip(tree_name, x_values, z_values):
            csv_writer.writerow([x, z, label])

    # Show the plot
    if plot:
        plt.show()

def init_trees_dont_write_yet_original(foliage_file, threepg=True, plot=False):
    """
        Takes in a tree_chart csv, outputs a series of random tree placements to a CSV (name,x,y)
        Can use 3pg, can create a scatter plot visualization
        Used for initial placement of trees to apply 3PG
    """
    # Generate random data for the x and z coordinates
    np.random.seed(42)
    num_trees = 50
    x_values = np.random.rand(num_trees)
    z_values = np.random.rand(num_trees)
    if threepg: 
        # use species data instead of Treelist. TODO make these the same class
        treelist = parse_species_data(foliage_file)
        tree_names = get_tree_names(treelist)
    else:
        treelist = TreeList(parse_csv_file(foliage_file))
        tree_names = treelist.get_tree_names()
    tree_name = np.random.choice(tree_names, num_trees)  # Randomly select tree names

    # ============ PLOTTING STUFF ===============
    if plot:
        # Define colors for each label
        label_colors = {label: plt.colormaps.get_cmap('viridis')(i / len(tree_names)) for i, label in enumerate(tree_names)}

        # Create a scatter plot with colored points
        for label, color in label_colors.items():
            plt.scatter(x_values[tree_name == label], z_values[tree_name == label], label=label, color=color)

        # Add labels and title
        plt.title('Initial Tree Placement')

        # Add legend
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()  # Adjust layout to prevent clipping

        # Save the plot to a file (optional)
        #plt.savefig('initial_tree_placement.png')

    # Show the plot
    if plot:
        plt.show()

    rows = [['name', 'x', 'z']]
    for x, z, label in zip(tree_name, x_values, z_values):
        rows.append([x, z, label])
    return rows

def init_trees_dont_write_yet(foliage_file, threepg=True, plot=False):
    """
        Takes in a tree_chart csv, outputs a series of random tree placements to a CSV (name,x,y)
        Can use 3pg, can create a scatter plot visualization
        Used for initial placement of trees to apply 3PG
        NEW VERSION SORTS THE ENTRIES SO THAT THEY ARE GROUPED BY TREE NAME
    """
    # Generate random data for the x and z coordinates
    np.random.seed(42)
    num_trees = 50
    x_values = np.random.rand(num_trees)
    z_values = np.random.rand(num_trees)
    if threepg: 
        # use species data instead of Treelist. TODO make these the same class
        treelist = parse_species_data(foliage_file)
        tree_names = get_tree_names(treelist)
    else:
        treelist = TreeList(parse_csv_file(foliage_file))
        tree_names = treelist.get_tree_names()
    tree_name = np.random.choice(tree_names, num_trees)  # Randomly select tree names

    # Sort tree_name and corresponding x_values and z_values by tree_name
    sorted_indices = np.argsort(tree_name)
    tree_name = tree_name[sorted_indices]
    x_values = x_values[sorted_indices]
    z_values = z_values[sorted_indices]

    # ============ PLOTTING STUFF ===============
    if plot:
        # Define colors for each label
        label_colors = {label: plt.colormaps.get_cmap('viridis')(i / len(tree_names)) for i, label in enumerate(tree_names)}

        # Create a scatter plot with colored points
        for label, color in label_colors.items():
            plt.scatter(x_values[tree_name == label], z_values[tree_name == label], label=label, color=color)

        # Add labels and title
        plt.title('Initial Tree Placement')

        # Add legend
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()  # Adjust layout to prevent clipping

        # Save the plot to a file (optional)
        #plt.savefig('initial_tree_placement.png')

        # Show the plot
        plt.show()

    # Prepare rows for output
    rows = [['name','x', 'z']]
    for x, z, label in zip(x_values, z_values, tree_name):
        rows.append([label, x, z])

    return rows

# Example usage:
#init_trees('foliage_data.csv', 'output_data.csv')
