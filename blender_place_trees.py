"""
File name: blender_place_trees.py
Author: Grace Todd
Date: May 9, 2024
Description: This file aims to test out different scripts for the Blender API, so that I can hopefully 
            Use Blender to generate the different tree assets and host the forest
            Because I think that would be really cool
"""

import bpy
import bmesh
import csv
import sys

sys.path.append('C:/Users/Grace/Documents/Masters_Project/foliager/')
input_filepath ="C:/Users/Grace/Documents/Masters_Project/foliager/test_data/OUTPUT_DATA.csv"

#import foliager

FOREST_FLOOR_SCALE =  30
POINT_IN_TIME = 24

def create_forest_floor():

    # Create a new mesh data
    ff_mesh_data = bpy.data.meshes.new(name="MeshData")

    # Create a new bmesh
    ff_bmesh = bmesh.new()

    # Create the "forest floor"
    ff_verts = [(-FOREST_FLOOR_SCALE, -FOREST_FLOOR_SCALE, 0), (FOREST_FLOOR_SCALE, -FOREST_FLOOR_SCALE, 0),\
     (FOREST_FLOOR_SCALE, FOREST_FLOOR_SCALE, 0), (-FOREST_FLOOR_SCALE, FOREST_FLOOR_SCALE, 0)]
    for v in ff_verts:
        ff_bmesh.verts.new(v)

    # Create edges and faces
    ff_bmesh.faces.new(ff_bmesh.verts)

    # Update the bmesh
    ff_bmesh.to_mesh(ff_mesh_data)
    ff_bmesh.free()

    # Create a new mesh object
    forest_floor = bpy.data.objects.new("ForestFloor", ff_mesh_data)

    # Link the mesh object to the scene
    scene = bpy.context.scene
    scene.collection.objects.link(forest_floor)

    # Set the location of the forest floor
    forest_floor.location = (0, 0, 0)  # center at origin

def create_canopy(name, x, y, height, dbh, live_crown_length, crown_diameter, tree_form, collection_name="Trees"):
# Check if a canopy object already exists
    if tree_form == '[\'pyramidal\']':
        p_canopy_objects = [obj for obj in bpy.data.objects if obj.name.startswith("Pyramidal_Canopy")]
        if p_canopy_objects:
            canopy = p_canopy_objects[0]  # Reuse the existing canopy object
        else:
            # Create the canopy
            canopy_filepath = "C:/Users/Grace/Documents/Masters_Project/foliager/blender/assets/pyramidal.obj"
            bpy.ops.wm.obj_import(filepath=canopy_filepath)

            # Get the canopy
            canopy = bpy.context.selected_objects[0]
            canopy.name = "Pyramidal_Canopy"  # Rename the canopy object
            # remove the canopy object from the scene
            # Hide the object in the viewport
            canopy.hide_set(True)
            canopy.hide_viewport = True

            # Hide the object in render
            canopy.hide_render = True
            
    elif tree_form == '[\'round\']':
        r_canopy_objects = [obj for obj in bpy.data.objects if obj.name.startswith("Round_Canopy")]
        if r_canopy_objects:
            canopy = r_canopy_objects[0]  # Reuse the existing canopy object
        else:
            # Create the canopy
            canopy_filepath = "C:/Users/Grace/Documents/Masters_Project/foliager/blender/assets/oval.obj"
            bpy.ops.wm.obj_import(filepath=canopy_filepath)

            # Get the canopy
            canopy = bpy.context.selected_objects[0]
            canopy.name = "Round_Canopy"  # Rename the canopy object
            
            # remove the canopy object from the scene
            # Hide the object in the viewport
            canopy.hide_set(True)
            canopy.hide_viewport = True

            # Hide the object in render
            canopy.hide_render = True
            
    else: 
        o_canopy_objects = [obj for obj in bpy.data.objects if obj.name.startswith("Other_Canopy")]
        if o_canopy_objects:
            canopy = o_canopy_objects[0]  # Reuse the existing canopy object
        else:
            # Create the canopy
            canopy_filepath = "C:/Users/Grace/Documents/Masters_Project/foliager/blender/assets/oval.obj"
            bpy.ops.wm.obj_import(filepath=canopy_filepath)

            # Get the canopy
            canopy = bpy.context.selected_objects[0]
            canopy.name = "Other_Canopy"  # Rename the canopy object

            # remove the canopy object from the scene
            # Hide the object in the viewport
            canopy.hide_set(True)
            canopy.hide_viewport = True

            # Hide the object in render
            canopy.hide_render = True
        
    # Shade smooth
    # bpy.context.view_layer.objects.active = canopy
    # bpy.ops.object.shade_smooth()

    # Set location and scale of the canopy
    canopy_height = height /3.3# Temporary solution!!!
    canopy.location = (x, y, canopy_height)
    canopy.scale = (crown_diameter, live_crown_length , crown_diameter) #x, z, y

    #canopy.name = name + '_canopy'
    
    return canopy

def create_trunk(name, x, y, height, dbh, live_crown_length, crown_diameter, tree_form, collection_name="Trees"):
    # Create the trunk
    trunk_filepath = "C:/Users/Grace/Documents/Masters_Project/foliager/blender/assets/trunk.obj"
    bpy.ops.wm.obj_import(filepath=trunk_filepath)

    # Get the trunk
    trunk = bpy.context.selected_objects[0]

    # Set location and scale of the imported object
    trunk_height = height - live_crown_length  # Adjusted height calculation
    trunk.scale = (dbh, height, dbh) #x, z, y? for some reason?
    trunk.location = (x, y, 0)  # Adjusted location to match canopy
    
    trunk.name = name + '_trunk'
    
    return trunk

def create_tree(name, x, y, height, dbh, live_crown_length, crown_diameter, tree_form, collection_name="Trees"):
    trunk = create_trunk(name, x, y, height, dbh, live_crown_length, crown_diameter, tree_form)
    canopy = create_canopy(name, x, y, height, dbh, live_crown_length, crown_diameter, tree_form)
    
    # Merge the trunk and canopy
    bpy.context.view_layer.objects.active = trunk
    bpy.ops.object.modifier_add(type='BOOLEAN')
    bpy.context.object.modifiers["Boolean"].operation = 'UNION'
    bpy.context.object.modifiers["Boolean"].object = canopy
    bpy.ops.object.modifier_apply(modifier="Boolean")
    
    tree = trunk
    tree.name = name
    
    return tree


def add_trees_to_collection(tree_list, collection_name="Trees"):
    # Check if the collection already exists
    if collection_name in bpy.data.collections:
        new_collection = bpy.data.collections[collection_name]
        bpy.context.scene.collection.children.link(new_collection)
    else:
        # Create a new collection for trees
        new_collection = bpy.data.collections.new(collection_name)
    
        # Link the new collection to the scene collection
        bpy.context.scene.collection.children.link(new_collection)
    
    # Link tree objects to the new collection and unlink from the scene collection
    for tree in tree_list:
        new_collection.objects.link(tree)
        bpy.context.scene.collection.objects.unlink(tree)


def gen_trees_in_blender(coordinates_filepath):
    
    create_forest_floor()
    
    collection_name = "Trees"
    # Create a new collection
    new_collection = bpy.data.collections.new(collection_name)

    # accumulate tree objects and location
    
    tree_list = []
    # Open the CSV file for reading
    with open(coordinates_filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            x = (float(row['x']) * FOREST_FLOOR_SCALE * 2) - FOREST_FLOOR_SCALE
            y = (float(row['z']) * FOREST_FLOOR_SCALE * 2) - FOREST_FLOOR_SCALE# counterintuitive but temporary -- with newer data files, I'll use y instead
            height = float(row['height'])
            dbh = float(row['dbh'])
            species_name = row['name']
            tree_key = row['tree_key']
            name = tree_key + '_' + species_name
            live_crown_length = float(row['lcl'])
            crown_diameter = float(row['c_diameter'])
            tree_form = row['q_tree_form']
            t = float(row['t'])
#            canopy = create_canopy(name, x, y, height, dbh, live_crown_length, crown_diameter, tree_form)
#            trunk = create_trunk(name, x, y, height, dbh, live_crown_length, crown_diameter,tree_form)
            if t == POINT_IN_TIME:
                tree = create_tree(name, x, y, height, dbh, live_crown_length, crown_diameter,tree_form)
                tree_list.append(tree)
    
    add_trees_to_collection(tree_list)

 
gen_trees_in_blender(input_filepath)