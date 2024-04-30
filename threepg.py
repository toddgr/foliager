"""
File name: blender_place_trees.py
Author: Grace Todd
Date: April 30, 2024
Description: This file aims to test out different scripts for the Blender API, so that I can hopefully 
            Use Blender to generate the different tree assets and host the forest
            Because I think that would be really cool
"""

import bpy
import bmesh
import csv

FOREST_FLOOR_SCALE = 20

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
    
    
def create_tree(x, y,dbh, height, name, collection_name="Trees"):
    # Path to the OBJ file
    obj_path = "C:/Users/Grace/Documents/Masters_Project/foliager/blender/default_tree.obj"

    # Import OBJ file
    bpy.ops.wm.obj_import(filepath=obj_path)

    # Get the imported object
    imported_obj = bpy.context.selected_objects[0]

    # Set location of the imported object
    imported_obj.location = (x, y, 0)  # Example coordinates
    
    imported_obj.scale = (dbh, height/15, dbh) #x, z, y? for some reason?
    imported_obj.name = name
    
    return imported_obj


def add_trees_to_collection(tree_list, collection_name="Trees"):
    scene_collection = bpy.context.scene.collection
    
    # Link the new collection to the scene collection
    scene_collection = bpy.context.scene.collection
    scene_collection.children.link(new_collection)
    
    collection = bpy.data.collections.get(collection_name)
    
    for tree in tree_list:
        collection.objects.link(tree)
        scene_collection.objects.unlink(tree)
   
    pass
    

if __name__ == "__main__":
    # filepaths
    coordinates_filepath = "C:/Users/Grace/Documents/Masters_Project/douglas_fir_plot_data.csv"
    
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
            y = (float(row['z']) * FOREST_FLOOR_SCALE * 2) - FOREST_FLOOR_SCALE # counterintuitive but temporary -- with newer data files, I'll use y instead
            height = float(row['height'])
            dbh = float(row['dbh'])
            name = row['name']
            tree = create_tree(x,y,dbh,height, name)
            tree_list.append(tree)
    
    add_trees_to_collection(tree_list, collection_name)