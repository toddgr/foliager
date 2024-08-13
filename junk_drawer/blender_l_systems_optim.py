import numpy as np
import bpy

def create_mesh(vertices, edges, name="Test_Tree"):
    """
        Turn the coordinates and edges into wireframe structures
    """
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

def add_thickness(obj, thickness=0.1):
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
    
    # Access the Skin Modifier
    skin_modifier = obj.modifiers["Skin"]
    
    # Enter Edit Mode to adjust vertex radii
    bpy.ops.object.mode_set(mode='EDIT')
    
    #  ===== insert trunk and branch scaling stuff here =====
    
    # Return to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    

    # Smooth out the tree
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 4
    
    # Apply the modifiers
    bpy.ops.object.modifier_apply(modifier="Skin")
    bpy.ops.object.modifier_apply(modifier="Subdivision")
    
    # Apply smooth shading
    bpy.ops.object.shade_smooth()

    return obj


def add_material(obj, material_name="defaultMat"):
    """ Applies a material to the new tree."""

    # Select the object
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Create a new red material
    material = bpy.data.materials.new(name="BrownMaterial")
    material.use_nodes = True  # Enable nodes for material (optional)
    
    # Set the material color to red
    nodes = material.node_tree.nodes
    bsdf_node = nodes.get('Principled BSDF')
    if bsdf_node:
        bsdf_node.inputs['Base Color'].default_value = (0.259, 0.149, 0.008, 1)  # Red color with full opacity
    
    # Assign the material to the mesh
    if len(obj.data.materials) > 0:
        obj.data.materials[0] = material
    else:
        obj.data.materials.append(material)

    return obj

def rotate_vector(vector, axis, angle_rad):
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

def plot_l_system(angle_deg, string):
    """
        Take the L system string and give coordinates and edges
        to the series of points for use in Blender
    """
    step_length = 1
    angle_rad = np.radians(angle_deg)
    
    # Directions for 3D: Forward, Right, Up
    directions = np.array([
        [1, 0, 0],  # X axis
        [0, 1, 0],  # Y axis
        [0, 0, 1]   # Z axis
    ])
    direction_index = 0  # Start facing along X axis
    position = np.array([0.0, 0.0, 0.0])
    
    coordinates = [tuple(position)]
    coordinates_map = {tuple(position): 0}
    edges = []
    stack = []
    current_index = 0

    for char in string:
        if char == 'F':
            new_position = tuple(position + directions[direction_index] * step_length)
            if new_position not in coordinates_map:
                current_index += 1
                coordinates.append(new_position)
                coordinates_map[new_position] = current_index

            edges.append((coordinates_map[tuple(position)], coordinates_map[new_position]))
            position = new_position

        elif char == '+':
            directions = np.array([rotate_vector(d, 'z', angle_rad) for d in directions])
        elif char == '-':
            directions = np.array([rotate_vector(d, 'z', -angle_rad) for d in directions])
        elif char == '\\':
            directions = np.array([rotate_vector(d, 'x', -angle_rad) for d in directions])
        elif char == '/':
            directions = np.array([rotate_vector(d, 'y', angle_rad) for d in directions])
        elif char == '^':
            directions = np.array([rotate_vector(d, 'x', angle_rad) for d in directions])
        elif char == '&':
            directions = np.array([rotate_vector(d, 'y', -angle_rad) for d in directions])
        elif char == '[':  # new branch
            stack.append((position, direction_index, directions.copy()))
        elif char == ']':  # end of new branch
            position, direction_index, directions = stack.pop()

    print(coordinates)
    return coordinates, edges


def generate_l_system(n, d, axiom, rules):
    """
        n = number of iterations
        d = degrees
        axiom = the initial string
        rules = dict of production rules
    """
    
    # Rewrite the string for every iteration
    for _ in range(n):
        new_axiom = ''
        print(f'===== ITERATION {_} =====')
        print(f'current axiom: {axiom}')
        # apply production rules
        # for char in axiom:
        #     if char in rules:
        #         axiom.replace(char, rules[char])
        for char in axiom:
            #print(f'current char: {char}')
            if char in rules:
                new_char = rules[char]
                #print(f'replacing {char} with {rules[char]}')
                new_axiom += new_char
            else:
                new_axiom += char

        axiom = new_axiom
        print(f'next axiom: {new_axiom}')
    
    
    string=new_axiom
    print(f'final instructions: {string}')

    # Interpret each instruction into coordinates and edges
    print("Creating coordinates...")
    coordinates, edges = plot_l_system(d, string)

    return coordinates, edges


def create_axiom_and_rules(dbh=1, lcl=2, c_diam=2, height=4, shape='cone'):
    """ Input: Calculated 3-PG parameters that define the dimensions
               of the tree
        Output: L systems parameters to generate trees from.
    """

    # each tree shape will have their own axiom rules to follow
    if shape == 'cone': 
        n = 7 # number of iterations
        d = 25.7


        axiom = 'X'
        rules = {'X': 'F[+X][-X]FX','F':'FF'}
    elif shape == 'round':
        pass
    elif shape == 'oval':
        pass
    elif shape == 'pyramidal':
        pass
    else: # irregular
        pass


    """ Reference
        X: The entire tree
        Y: The starts of the branches
        Z: The extensions of the branches
    """

    return n, d, axiom, rules


if __name__ == '__main__':
    # example usage
    n, d, axiom, rules = create_axiom_and_rules()
    vertices, edges = generate_l_system(n, d, axiom, rules)
    #plot_3d_coordinates_and_edges(vertices, edges)

    # Call the function
    tree = create_mesh(vertices, edges)
    tree = add_thickness(tree)
    tree = add_material(tree)