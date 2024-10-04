"""
File name: blender_shader_generator.py
Author: Grace Todd
Date: October 4, 2024
Description: This file uses Blender Shader nodes to procedurally generate tree bark textures.
            create_node() and link_nodes() based on functions created by blender_plus_python:
            https://github.com/CGArtPython/blender_plus_python/blob/main/geo_nodes/subdivided_triangulated_cube

            Adapted from bark texture developed by Ryan King Art on YouTube (Jul 4, 2022):
            https://www.youtube.com/watch?v=6ECeHoATa74
"""

import bpy

SPACING = 250

def create_node(node_tree, node_location, type_name):
    node_obj = node_tree.nodes.new(type=type_name)
    node_obj.location.x = node_location
    node_location += SPACING

    return node_obj, node_location

def link_nodes(node_tree, from_node, from_type, to_node, to_type):
    node_tree.links.new(from_node.outputs[from_type], to_node.inputs[to_type])

def create_shader(obj, tree=None):
    if tree:
        material = bpy.data.materials.new(name=tree.bark_texture[0])
    else:
        material = bpy.data.materials.new(name="empty_material")

    # Enable 'Use Nodes' to use the Principled BSDF shader
    material.use_nodes = True
    nodes = material.node_tree.nodes
    bsdf = nodes.get('Principled BSDF')


    # ========

    # Assign the material to the object
    if obj.data.materials:
        # Replace the existing material if any
        obj.data.materials[0] = material
    else:
        # Add the new material
        obj.data.materials.append(material)


if __name__ == '__main__':
    # Create a UV Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0,0,0))
    bpy.ops.object.shade_smooth()
    
    # Get the created sphere object
    sphere = bpy.context.object
    
    create_shader(sphere)