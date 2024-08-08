"""
File: l_systems_test.py
Author: Grace Todd
Date: August 8, 2024
Description: A sandbox for creating an l systems class that allows for
            procedural tree generation.
"""

import numpy as np

def generate_l_system(n, d, axiom, rules):
    """
        n = number of iterations
        d = degrees
        axiom = the initial string
        rules = dict of production rules
    """

    # Rewrite the string for every iteration

    for _ in range(n):
        print(f'current axiom: {axiom}')
        # apply production rules
        # for char in axiom:
        #     if char in rules:
        #         axiom.replace(char, rules[char])
        for char in rules:
            new_axiom = axiom.replace(char, rules[char])
            print(f'replacing {char} with {rules[char]}')

        axiom = new_axiom
        print(f'next axiom: {new_axiom}')
    
    print(f'final instructions: {axiom}')
    string=axiom

    # Interpret each instruction into coordinates and edges
    coordinates, edges = plot_l_system(d, string)
    print("Coordinates:", coordinates)
    print("Edges:", edges)
    
    plot_3d_coordinates_and_edges(coordinates, edges)

def rotate_vector(vector, axis, angle_deg):
    angle_rad = np.radians(angle_deg)
    cos_theta = np.cos(angle_rad)
    sin_theta = np.sin(angle_rad)
    
    if axis == 'x':
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, cos_theta, -sin_theta],
            [0, sin_theta, cos_theta]
        ])
    elif axis == 'y':
        rotation_matrix = np.array([
            [cos_theta, 0, sin_theta],
            [0, 1, 0],
            [-sin_theta, 0, cos_theta]
        ])
    elif axis == 'z':
        rotation_matrix = np.array([
            [cos_theta, -sin_theta, 0],
            [sin_theta, cos_theta, 0],
            [0, 0, 1]
        ])
    
    return np.dot(rotation_matrix, vector)


def round_and_format_coordinates(coordinates, decimals=3):
    formatted_coordinates = []
    for point in coordinates:
        formatted_point = tuple(round(coord, decimals) for coord in point)
        # Convert -0.0 to 0.0
        formatted_point = tuple(0.0 if coord == -0.0 else coord for coord in formatted_point)
        formatted_coordinates.append(formatted_point)
    return formatted_coordinates

def round_and_format_position(tpl, decimals=3):
    return tuple(0.0 if round(value, decimals) == -0.0 else round(value, decimals) for value in tpl)

def find_key_by_value(d, target_value):
    # Iterate through the dictionary items
    for key, value in d.items():
        if value == target_value:
            return key
    return None  # (Return None if the value is not found)

def plot_l_system(angle, string):
    """
        Turn the L system string into coordinates and edges
        d = degree to be turned
        string = string of commands
    """
    step_length = 10 # how much to increase each point by
    coordinates = [
        (0, 0, 0) # starting point
    ] # x-y-z of points
    edges = [] # (start, end) of edges

 
    # Directions for 3D: Forward, Right, Up
    directions = np.array([
        [1, 0, 0],  # X axis
        [0, 1, 0],  # Y axis
        [0, 0, 1]   # Z axis
    ])
    direction_index = 0  # Start facing along X axis
    position = np.array([0.0, 0.0, 0.0])
    coordinates = [tuple(position)]
    coordinates_map = {0:coordinates[0]}
    edges = []
    stack = []
    i = 0

    for char in string:
        if char == 'F':
            new_position = tuple(position + directions[direction_index] * step_length)
            coordinates = round_and_format_coordinates(coordinates)
            new_position = round_and_format_position(new_position)
            if new_position not in coordinates_map.values():
                i += 1
                coordinates.append(tuple(new_position))
                coordinates_map[i] = coordinates[i]

            edges.append((find_key_by_value(coordinates_map, tuple(position)), find_key_by_value(coordinates_map, new_position)))
            position = new_position
            
        elif char == '+':
            # Rotate around the Z axis
            directions = np.array([rotate_vector(d, 'z', angle) for d in directions])
        elif char == '-':
            # Rotate around the Z axis
            directions = np.array([rotate_vector(d, 'z', -angle) for d in directions])
        elif char == '[': # new branch
            saved_position = position
            stack.append((saved_position, direction_index, directions.copy()))
        elif char == ']': # end of new branch
            position, direction_index, directions = stack.pop()

    # round the coordinates
    return coordinates, edges

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_3d_coordinates_and_edges(coordinates, edges):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot coordinates
    x_coords, y_coords, z_coords = zip(*coordinates)
    # ax.scatter(x_coords, y_coords, z_coords, color='blue', label='Coordinates')
    
    # Plot edges
    for edge in edges:
        x_values = [coordinates[edge[0]][0], coordinates[edge[1]][0]]
        y_values = [coordinates[edge[0]][1], coordinates[edge[1]][1]]
        z_values = [coordinates[edge[0]][2], coordinates[edge[1]][2]]
        ax.plot(x_values, y_values, z_values, color='black', linestyle='-', linewidth=1)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Coordinates and Edges')
    plt.legend()
    plt.show()



if __name__ == '__main__':
    # test - generating a quadratic koch island
    n = 4
    d = 22.5
    axiom = 'F'
    rules = {'F':'FF-[-F+F+F]+[+F-F-F]'}

    generate_l_system(n, d, axiom, rules)