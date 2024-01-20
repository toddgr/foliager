import matplotlib.pyplot as plt
import numpy as np

# Generate random data
np.random.seed(42)  # Set seed for reproducibility
num_points = 50
x_values = np.random.rand(num_points)
y_values = np.random.rand(num_points)
labels = [f'Point {i+1}' for i in range(num_points)]

# Create a scatter plot
plt.scatter(x_values, y_values)

# Add labels to each point
for label, x, y in zip(labels, x_values, y_values):
    plt.annotate(label, (x, y), textcoords="offset points", xytext=(0, 5), ha='center')

# Add labels and title
plt.xlabel('X-axis Label')
plt.ylabel('Y-axis Label')
plt.title('Scatter Plot with Random Values')

# Show the plot
plt.show()
