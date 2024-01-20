import matplotlib.pyplot as plt
import numpy as np

# Generate random data
np.random.seed(42)
num_points = 50
x_values = np.random.rand(num_points)
y_values = np.random.rand(num_points)
labels = np.random.randint(1, 4, num_points)  # Random labels (assuming there are 3 categories)

# Define colors for each label
label_colors = {1: 'red', 2: 'green', 3: 'blue'}

# Create a scatter plot with colored points
for label, color in label_colors.items():
    plt.scatter(x_values[labels == label], y_values[labels == label], label=f'Label {label}', color=color)

# Add labels and title
plt.xlabel('X-axis Label')
plt.ylabel('Y-axis Label')
plt.title('Scatter Plot with Color Key')

# Add legend
plt.legend()

# Show the plot
plt.show()
