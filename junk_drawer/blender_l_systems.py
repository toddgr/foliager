"""
File: blender_l_systems.py
Author: Grace Todd
Date: August 12, 2024
Description: Taking what we did in l_systems_test and attempting to put it
            in Blender.
"""

import bpy
import numpy as np

def create_mesh(vertices, edges, name="Test_Tree"):
    # For debugging purposes
    # Delete any existing objects with the same name
    if name in bpy.data.objects:
        obj_to_delete = bpy.data.objects[name]
        
        # Unlink the object from all collections it is in
        for collection in obj_to_delete.users_collection:
            collection.objects.unlink(obj_to_delete)
        
        # Delete the object itself
        bpy.data.objects.remove(obj_to_delete, do_unlink=True)
    
    # Create a new mesh
    mesh = bpy.data.meshes.new(name + "Mesh")
    
    # Create a new object with the mesh
    obj = bpy.data.objects.new(name, mesh)
    
    # Link the object to the active scene
    bpy.context.collection.objects.link(obj)
    
    # Create the mesh from given vertices and edges
    mesh.from_pydata(vertices, edges, [])
    
    # Update the mesh with new data
    mesh.update()

    return obj

def add_thickness(obj):
    """
        Once we have our coordinates in blender space, 
        we can start to model the tree.
        This function turns lines into solid objects.
    """
    # Select the object
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Apply the Skin Modifier
    bpy.ops.object.modifier_add(type='SKIN')
    
    # Smooth out the tree
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 4
    
    # Apply the modifiers
    bpy.ops.object.modifier_apply(modifier="Skin")
    bpy.ops.object.modifier_apply(modifier="Subdivision")
    
    # Apply smooth shading
    bpy.ops.object.shade_smooth()

    return obj

def generate_l_system(n, d, axiom, rules):
    """
        n = number of iterations
        d = degrees
        axiom = the initial string
        rules = dict of production rules
    """
    new_axiom = ''
    # Rewrite the string for every iteration
    for _ in range(n):
        print(f'current axiom: {axiom}')
        # apply production rules
        # for char in axiom:
        #     if char in rules:
        #         axiom.replace(char, rules[char])
        for char in axiom:
            print(f'current char: {char}')
            if char in rules:
                new_char = rules[char]
                print(f'replacing {char} with {rules[char]}')
                new_axiom += new_char
            else:
                new_axiom += char

        axiom = new_axiom
        print(f'next axiom: {new_axiom}')
    
    print(f'final instructions: {new_axiom}')
    string=new_axiom

    # Interpret each instruction into coordinates and edges
    print("Creating coordinates...")
    coordinates, edges = plot_l_system(d, string)

    return coordinates, edges

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
    step_length = 1 # how much to increase each point by
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
        elif char == '\\':
            # Rotate around the X axis
            directions = np.array([rotate_vector(d, 'x', -angle) for d in directions])
        elif char == '/':
            # Rotate around the Y axis
            directions = np.array([rotate_vector(d, 'y', angle) for d in directions])
        elif char == '^':
            # Rotate around the X axis (upward)
            directions = np.array([rotate_vector(d, 'x', angle) for d in directions])
        elif char == '&':
            # Rotate around the Y axis (downward)
            directions = np.array([rotate_vector(d, 'y', -angle) for d in directions])
        elif char == '[': # new branch
            saved_position = position
            stack.append((position, direction_index, directions.copy()))
        elif char == ']': # end of new branch
            position, direction_index, directions = stack.pop()

    # round the coordinates
    return coordinates, edges


if __name__ == '__main__':
    # example usage
    n = 4
    d = 90
    axiom = 'X'
    rules = {'X':'&F\\+Y+Y+Y+Y^FF/', 'Y':'[FF]'}

    vertices, edges = generate_l_system(n, d, axiom, rules)

    # Call the function
    tree = create_mesh(vertices, edges)
    add_thickness(tree)