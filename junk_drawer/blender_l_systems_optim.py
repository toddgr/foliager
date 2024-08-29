import numpy as np
import random
import bpy
import bmesh
import math

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

def add_thickness(obj, thickness=1):
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
    
    # Select all vertices
    bpy.ops.mesh.select_all(action='SELECT')
    
    # # Adjust the radius of the selected vertices
    # bpy.ops.transform.resize(value=(thickness, thickness, thickness))
    
    # # Return to Object Mode
    # bpy.ops.object.mode_set(mode='OBJECT')
    
    # # Smooth out the tree
    # bpy.ops.object.modifier_add(type='SUBSURF')
    # bpy.context.object.modifiers["Subdivision"].levels = 1
    
    # # Apply the modifiers
    # bpy.ops.object.modifier_apply(modifier="Skin")
    # bpy.ops.object.modifier_apply(modifier="Subdivision")
    
    # # Apply smooth shading
    # bpy.ops.object.shade_smooth()

    return obj



def assign_texture(obj_name, color='brown', texture=None):
    """ Assigns the bark texture to the tree with smart UV projection
        Input: tree object name, /path/to/image/texture
        Output: tree object with new color/texture/both
    """
    mix_factor = 1.

    #TODO Add more specific textures when trunk thickness is implemented    
        # Texture paths for different texture types
    texture_paths = {
        'smooth': 'C:/Users/Grace/Downloads/texture-smooth.png',
        'lenticels': 'C:/Users/Grace/Downloads/texture-smooth.png',
        'furrows': 'C:/Users/Grace/Downloads/texture-furrows.jpg',
        'ridges': 'C:/Users/Grace/Downloads/texture-furrows.jpg',
        'cracks': 'C:/Users/Grace/Downloads/texture-furrows.jpg',
        'scales': 'C:/Users/Grace/Downloads/texture-furrows.jpg',
        'strips': 'C:/Users/Grace/Downloads/texture-furrows.jpg',
    }

    # Color mappings for different color names
    color_mappings = {
        'gray': (0.231, 0.22, 0.165, 1),
        'white': (0.831, 0.765, 0.671, 1),
        'red': (0.451, 0.094, 0.024, 1),
        'brown': (0.259, 0.149, 0.008, 1),  # Default color
        'green': (0.047, 0.522, 0.075, 1) # Leaf color
    }
    
    # Get the object
    obj = bpy.data.objects.get(obj_name)
    if obj is None:
        print(f"Object '{obj_name}' not found.")
        return
    
    # Set the object to active and in edit mode for unwrapping
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Select all faces
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Apply Smart UV Project
    bpy.ops.uv.smart_project(angle_limit=75.0, island_margin=0.0)
    
    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Check if the object has a material
    if not obj.data.materials:
        mat = bpy.data.materials.new(name="Material")
        obj.data.materials.append(mat)
    else:
        mat = obj.data.materials[0]
    
    # Enable 'Use Nodes' in the material
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    
    # Clear existing nodes (if any)
    for node in nodes:
        nodes.remove(node)
    
    # Add nodes for BSDF and output
    bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    
    # Set node positions 
    # (just to help with organization in case we want to use the UI to change it)
    bsdf_node.location = (0, 300)
    output_node.location = (300, 300)
    
    # Set color or texture (or both)
    if texture and texture in texture_paths:
        tex_image_node = nodes.new(type='ShaderNodeTexImage')
        mix_rgb_node = nodes.new(type='ShaderNodeMixRGB')
        rgb_node = nodes.new(type='ShaderNodeRGB')
        
        tex_image_node.location = (-600, 300)
        mix_rgb_node.location = (-300, 300)
        rgb_node.location = (-600, 100)
        
        # Configure the RGB node
        rgba_color = color_mappings.get(color, color_mappings[color])
        color_variation = 0.05
        rgba_color = (
            max(0, min(1, rgba_color[0] + random.uniform(-color_variation, color_variation))),
            max(0, min(1, rgba_color[1] + random.uniform(-color_variation, color_variation))),
            max(0, min(1, rgba_color[2] + random.uniform(-color_variation, color_variation))),
            rgba_color[3]  # Alpha value remains unchanged
        )
        rgb_node.outputs['Color'].default_value = rgba_color
        
        # Configure the MixRGB node
        mix_rgb_node.inputs['Fac'].default_value = mix_factor
        mix_rgb_node.blend_type = 'MULTIPLY'  # Or any other blend type you want
        
        # Link the nodes
        links = mat.node_tree.links
        links.new(tex_image_node.outputs['Color'], mix_rgb_node.inputs['Color1'])
        links.new(rgb_node.outputs['Color'], mix_rgb_node.inputs['Color2'])
        links.new(mix_rgb_node.outputs['Color'], bsdf_node.inputs['Base Color'])
        links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
        
        # Load the image and assign it to the texture node
        image_path = texture_paths[texture]    
        image = bpy.data.images.load(image_path)
        tex_image_node.image = image
    
    else:
        # No texture, just use the default color (brown)
        links = mat.node_tree.links
        rgba_color = color_mappings.get(color, color_mappings[color])
        color_variation = 0.05
        rgba_color = (
            max(0, min(1, rgba_color[0] + random.uniform(-color_variation, color_variation))),
            max(0, min(1, rgba_color[1] + random.uniform(-color_variation, color_variation))),
            max(0, min(1, rgba_color[2] + random.uniform(-color_variation, color_variation))),
            rgba_color[3]  # Alpha value remains unchanged
        )
        bsdf_node.inputs['Base Color'].default_value = rgba_color
    
    # Final link to output
    links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])


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
    max_deviation = np.radians(20)  # How much the random angle can deviate from original

    # Directions for 3D: Forward, Right, Up
    directions = np.array([
        [1, 0, 0],  # X axis
        [0, 1, 0],  # Y axis
        [0, 0, 1]   # Z axis
    ])
    direction_index = 2  # Start facing along X axis
    position = np.array([0.0, 0.0, 0.0])
    
    coordinates = [tuple(position)]
    coordinates_map = {tuple(position): 0}
    leaves = []
    edges = []
    stack = []
    current_index = 0

    for char in string:
        # Randomize the angle a little bit
        rand_angle = random.uniform(angle_rad - max_deviation, angle_rad + max_deviation)
        if char == 'F':
            new_position = tuple(position + directions[direction_index] * step_length)
            if new_position not in coordinates_map:
                current_index += 1
                coordinates.append(new_position)
                coordinates_map[new_position] = current_index

            edges.append((coordinates_map[tuple(position)], coordinates_map[new_position]))
            position = new_position

        elif char == '+': # z axis
            directions = np.array([rotate_vector(d, 'z', rand_angle) for d in directions])
        elif char == '-': # z axis
            directions = np.array([rotate_vector(d, 'z', -rand_angle) for d in directions])
        elif char == '\\': # x axis
            directions = np.array([rotate_vector(d, 'x', -rand_angle) for d in directions])
        elif char == '/': # y axis
            directions = np.array([rotate_vector(d, 'y', rand_angle) for d in directions])
        elif char == '^': # x axis (up)
            directions = np.array([rotate_vector(d, 'x', rand_angle) for d in directions])
        elif char == '&': # y axis (up
            directions = np.array([rotate_vector(d, 'y', -rand_angle) for d in directions])
        elif char == '[':  # new branch
            stack.append((position, direction_index, directions.copy()))
        elif char == ']':  # end of new branch
            position, direction_index, directions = stack.pop()
        elif char == '*': # leaf
            leaves.append(position)

    print(leaves)
    return coordinates, edges, leaves


def generate_l_system(n, d, axiom, rules):
    """
        n = number of iterations
        d = degrees
        axiom = the initial string
        rules = dict of production rules
    """
    
    # Rewrite the string for every iteration
    new_axiom = ''
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
    coordinates, edges, leaves = plot_l_system(d, string)

    return coordinates, edges, leaves


def create_axiom_and_rules(dbh, lcl, c_diam, height, branch_spacing=2, shape='dimension_test'):
    """ Input: Calculated 3-PG parameters that define the dimensions
               of the tree
        Output: L systems parameters to generate trees from.
        
        Branch spacing has to be evenly divided by the lcl to work 
    """

    # height will determine the height of the trunk
    # dbh will determine the diameter of the trunk
    # lcl will determine the height of the live crown
    # c_diam will determine the diameter of the live crown

    # each tree shape will have their own axiom rules to follow
    if shape == 'cone': 
        n =  2 # number of iterations
        d = 30
        axiom = 'FX'
        rules = {'X': 'F[+B][-B]F[+/B][-/B]F[+&B][-&B]X', 'L':'LF','B':'[+L+F]F[-L-F]F[+L+F]F[-L-F]'}
        
    elif shape == 'old_round':
        # step length 5
        n = 5 # number of iterations
        d = -60
        axiom = 'FFFFFA'
        rules = {'A': 'FB[F+A]B[F-A]B[F/A]B[F&A]', 'B': 'BB'}
        
    elif shape == 'oval':
        n = 3 # number of iterations (stay at 3, looks prettiest at 4)
        d = 30
        axiom = 'FX'
        rules = {'X': 'F[++B][--B][+//B][-//B][+&&B][-&&B]F[++B][--B][+//B][-//B][+&&B][-&&B]F[++B][--B][+//B][-//B][+&&B][-&&B]F[++B][--B][+//B][-//B][+&&B][-&&B]X','F':'FF', 'B':'F[+B]F[-B]F[+B]F[-B]'}
        
    elif shape == 'pyramidal':
        n =  6 # number of iterations
        d =  50
        axiom = 'X'
        rules = {'X': '[+B]F[-B]F[+/B]F[-/B]F[+&B]F[-&B]X', 'L':'LF','B':'[L+F]F[L-F]F[L+F]F[L-F]'}
        
    elif shape == 'dimension_test' or shape == 'leaf_test':
        n = 2 # 1 gets the trunk, 2 gets the branches 
        d = 45
        trunk = create_trunk(height)
        branch = create_branch(c_diam, lcl, shape)
        
        branches = create_branches(branch)
        #branch_iter = 'BF' * lcl
        branch_iter = ('B' + ('F' * branch_spacing)) * int(lcl / branch_spacing)
        
        axiom = 'TX'
        rules = {'T':trunk, 'B':branches, 'X':branch_iter}
        
    elif shape=="round":
        # step length 5
        n = 3 # number of iterations
        d = 60
        
        trunk = create_trunk(height)
        branch = create_branch(c_diam, lcl, shape)
        
        branches = create_branches(branch)
        #branch_iter = 'BF' * lcl
        branch_iter = ('B' + ('F' * branch_spacing)) * int(lcl / branch_spacing)
        
        axiom = 'TX'
        rules = {'T':trunk, 'B':branches, 'X':branch_iter}
        
        #axiom = 'FFFFFA'
        #rules = {'A': 'FB[F+A]B[F-A]B[F/A]B[F&A]', 'B': 'BB'}
        
    else: # irregular
        pass

    return n, d, axiom, rules


def create_trunk(height):
    """
        Takes in height of the trunk of a tree, returns the string
        for L system to create the proper trunk size
    """
    return 'F' * int(height)


def create_branches(branch):
    """ makes branches in all directions """
    branches = put_in_branch(add_yaw(add_roll(branch))) + put_in_branch(add_yaw(add_roll(branch, '&'), '-'))\
        + put_in_branch(add_yaw(add_pitch(add_roll(branch)))) + put_in_branch(add_yaw(add_pitch(add_roll(branch, '&')), '-'))\
        + put_in_branch(add_yaw(add_pitch(add_roll(branch), '^'))) + put_in_branch(add_yaw(add_pitch(add_roll(branch, '&'), '^'), '-'))
    return branches


def create_branch(c_diam, lcl, shape):
    """
         Takes in the dimensions for live crown, 
         Returns string for L system to generate a branch
    """
    branch = ''
    
    if shape == 'dimension_test':
        #branch += ('F[+F][-F]' * random.randint(int(c_diam/2)-2, int(c_diam/2)))
        branch += ('F' * random.randint(int(c_diam/2)-2, (int(c_diam/2))+1))
        #for _ in range(int(c_diam/4)):
            #branch += 'F[+F]F[-F]'

    if shape == 'leaf_test':
        #branch += ('F[+F][-F]' * random.randint(int(c_diam/2)-2, int(c_diam/2)))
        branch += ('F' * random.randint(int(c_diam/2)-2, (int(c_diam/2))+1)) + '*'
        #for _ in range(int(c_diam/4)):
            #branch += 'F[+F]F[-F]'
            
    elif shape == 'round':
        for _ in range(int(c_diam/2)):
            sub_branch = int(c_diam/2) - _
            branch += 'F[+' + ('F' * sub_branch) + '][-' + ('F' * sub_branch) + '][/' + ('F' * sub_branch) +'][&' + ('F' * sub_branch) + ']'
    
    #return 'F' * int (c_diam/2)
    return branch


def add_pitch(word, sign='\\'):
    # x axis
    if sign=='\\':
        return '\\' + word
    return '^' + word


def add_roll(word, sign='/'):
    # y axis
    if sign=='/':
        return '/' + word
    return '&' + word


def add_yaw(word, sign='+'):
    # z axis
    if sign == '+':    
        return '+' + word
    return '-' + word

def put_in_branch(word):
    return '[' + word + ']'


def place_leaves(coordinates):
    """
    Takes in a list of coordinates, places leaves in those positions.
    """
    radius = 1
    
    # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')
    
    # Select all mesh objects in the scene
    for obj in bpy.data.objects:
        if "Sphere" in obj.name:
            obj.select_set(True)
    
    # Delete selected objects
    bpy.ops.object.delete()
    
    for coords in coordinates:
        x, y, z = coords
        
        # Create a sphere at the given coordinates
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(x, y, z))
        
        # Get the reference to the newly created object
        obj = bpy.context.object
        assign_texture(obj.name, 'green')
        
    # Apply smooth shading
    bpy.ops.object.shade_smooth()
        

def add_trunk_thickness(obj, total_height, thickness=1):
    """
    This function turns lines into solid objects by adding a Skin Modifier and
    resizing trunk to match 3-PG dimensions.
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
    
    # Get the BMesh from the object
    bm = bmesh.from_edit_mesh(obj.data)
    
    # Deselect all vertices first
    for v in bm.verts:
        v.select_set(False)
    
    # Select vertices with x and y coordinates of 0
    for v in bm.verts:
        if abs(v.co.x) < 1e-6 and abs(v.co.y) < 1e-6 and abs(v.co.z) < total_height - (total_height / 4):
            v.select_set(True)
    
    # Update the mesh to apply the selection
    bmesh.update_edit_mesh(obj.data)
    
    # Resize the selected vertices
    bpy.ops.transform.skin_resize(
        value=(thickness, thickness, thickness),
        orient_type='GLOBAL',
        orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
        orient_matrix_type='GLOBAL',
        mirror=True,
        use_proportional_edit=True,
        proportional_edit_falloff='INVERSE_SQUARE',
        proportional_size=thickness/2,
        use_proportional_connected=False,
        use_proportional_projected=False,
        snap=False,
        snap_elements={'INCREMENT'},
        use_snap_project=False,
        snap_target='CLOSEST',
        use_snap_self=True,
        use_snap_edit=True,
        use_snap_nonedit=True,
        use_snap_selectable=False
    )
    
    # Return to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Smooth out the tree
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 1
    
    # Apply the modifiers
    bpy.ops.object.modifier_apply(modifier="Skin")
    bpy.ops.object.modifier_apply(modifier="Subdivision")
    
    # Apply smooth shading
    bpy.ops.object.shade_smooth()

    return obj


def join_leaves_and_tree(name='Tree'):
    """ 
        Joins together all the leaves and the tree and renames it accordingly
    """
    
    # Deselect all objects first
    bpy.ops.object.select_all(action='DESELECT')
    
    # Select all mesh objects (assuming the leaves and tree are all meshes)
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and ("Sphere" in obj.name or name in obj.name):
            obj.select_set(True)
    
    # Join all selected objects
    bpy.ops.object.join()
    
    # Rename the active object (which is the result of the join operation)
    bpy.context.object.name = name
    
    return bpy.data.objects.get(name)


def build_tree(name, position, dbh, lcl, trunk_height, c_diam, bark_color, bark_texture):
    # create the l-system
    n, d, axiom, rules = create_axiom_and_rules(dbh, lcl, c_diam, trunk_height, shape='leaf_test')
    vertices, edges, leaves = generate_l_system(n, d, axiom, rules)

    # make the tree
    tree = create_mesh(vertices, edges, name)
    tree = add_trunk_thickness(tree, trunk_height+lcl, dbh)
    assign_texture(tree.name, bark_color, bark_texture)
    place_leaves(leaves)
    tree = join_leaves_and_tree(name)
    
    # Set the 3D cursor to the origin
    bpy.context.scene.cursor.location = (0, 0, 0)
    
    bpy.context.view_layer.objects.active = tree
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='BOUNDS')
    
    # Move the object to the specified location
    tree.location = position


if __name__ == '__main__':
    # example usage
    # Input the dimensions (replace this with 3-pg stuff later)
    dbh = 1.58402328222362
    lcl = 14.234187202330084
    trunk_height = 5
    c_diam = 15

    bark_color = 'gray'
    bark_texture = 'furrows'
    
    build_tree('Bigleaf Maple', (0, 0, 0), dbh, lcl, trunk_height, c_diam, bark_color, bark_texture)
    #build_tree('Tree2', (0,0,0), dbh, lcl, trunk_height, c_diam, bark_color, bark_texture)
    #build_tree('Tree3', (-10, -10,0), dbh, lcl, trunk_height, c_diam, bark_color, bark_texture)
        