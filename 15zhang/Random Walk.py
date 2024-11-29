import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Set the random seed for reproducibility
np.random.seed(0)

# Define the number of steps
num_steps = 1000

# Generate random step distances in x, y, and z directions
step_distances = np.random.uniform(-4, 4, size=(num_steps, 3))

# Calculate cumulative sum of step distances
positions = np.cumsum(step_distances, axis=0)

# Extract x, y, and z coordinates
x = positions[:, 0]
y = positions[:, 1]
z = positions[:, 2]

# Calculate color map based on number of steps
colors = np.arange(num_steps)

# Plot the random walk
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(x, y, z, c=colors, cmap='Blues', linewidths=0.5, alpha=0.7)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Three-Dimensional Random Walk')
fig.colorbar(scatter, label='Number of Steps')
plt.show()