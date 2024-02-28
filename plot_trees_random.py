import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tree_class import TreeList
from parse_tree_input import parse_csv_file

def init_trees(foliage_file):
    # Generate random data
    np.random.seed(42)
    num_points = 100
    x_values = np.random.rand(num_points)
    y_values = np.random.rand(num_points)
    treelist = TreeList(parse_csv_file(foliage_file))  # Name, Growth Rate, Average Lifespan
    tree_names = treelist.get_tree_names()
    labels = np.random.choice(tree_names, num_points)  # Randomly select tree names

    # Create a DataFrame to store the data
    # Could also initialize breast height and height and stuff here too, perhaps
    data = pd.DataFrame({'X': x_values, 'Y': y_values, 'Label': labels})

    # Save the DataFrame to a CSV file
    data.to_csv("scatter_plot_coordinates.csv", index=False)


    # Define colors for each label
    label_colors = {label: plt.colormaps.get_cmap('viridis')(i / len(tree_names)) for i, label in enumerate(tree_names)}

    # Create a scatter plot with colored points
    for label, color in label_colors.items():
        plt.scatter(x_values[labels == label], y_values[labels == label], label=label, color=color)


    # Add labels and title
    plt.title('Random Tree Placement')

    # Add legend
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()  # Adjust layout to prevent clipping

    # Show the plot
    plt.show()
