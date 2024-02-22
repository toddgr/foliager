# import matplotlib.pyplot as plt
# import numpy as np
# from tree_class import TreeList
# from parse_tree_input import parse_csv_file

# def init_trees(foliage_file):
#     # Generate random data
#     np.random.seed(42)
#     num_points = 100
#     x_values = np.random.rand(num_points)
#     y_values = np.random.rand(num_points)
#     treelist = TreeList(parse_csv_file(foliage_file))  # Name, Growth Rate, Average Lifespan
#     tree_names = treelist.get_tree_names()
#     labels = np.random.choice(tree_names, num_points)  # Randomly select tree names

#     # Define colors for each label
#     label_colors = {label: plt.colormaps.get_cmap('viridis')(i / len(tree_names)) for i, label in enumerate(tree_names)}

#     # Create a scatter plot with colored points
#     for label, color in label_colors.items():
#         plt.scatter(x_values[labels == label], y_values[labels == label], label=label, color=color)

#     # Add labels and title
#     plt.title('Initial Tree Placement')

#     # Add legend
#     plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
#     plt.tight_layout()  # Adjust layout to prevent clipping

#     # Show the plot
#     plt.show()

import numpy as np
import csv
import matplotlib.pyplot as plt
from tree_class import TreeList
from parse_tree_input import parse_csv_file

def init_trees(foliage_file, output_csv_file):
    """
        Takes in a tree_chart csv, outputs a series of random tree placements to a CSV (name,x,y)
        Used for initial placement of trees to apply 3PG
    """
    threepg = false # If true, use species data instead of Treelist. TODO make these the same class

    # Generate random data
    np.random.seed(42)
    num_trees = 50
    x_values = np.random.rand(num_trees)
    y_values = np.random.rand(num_trees)
    treelist = TreeList(parse_csv_file(foliage_file))  # Assuming TreeList and parse_csv_file functions are defined
    tree_names = treelist.get_tree_names()
    tree_name = np.random.choice(tree_names, num_trees)  # Randomly select tree names

    # Define colors for each label
    label_colors = {label: plt.colormaps.get_cmap('viridis')(i / len(tree_names)) for i, label in enumerate(tree_names)}

    # Create a scatter plot with colored points
    for label, color in label_colors.items():
        plt.scatter(x_values[tree_name == label], y_values[tree_name == label], label=label, color=color)

    # Add labels and title
    plt.title('Initial Tree Placement')

    # Add legend
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()  # Adjust layout to prevent clipping

    # Save the plot to a file (optional)
    # plt.savefig('initial_tree_placement.png')

    # Write x, y, and label data to CSV file
    with open(output_csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['name', 'x', 'y'])  # Write header
        for x, y, label in zip(tree_name, x_values, y_values):
            csv_writer.writerow([x, y, label])

    # Show the plot
    plt.show()

# Example usage:
#init_trees('foliage_data.csv', 'output_data.csv')
