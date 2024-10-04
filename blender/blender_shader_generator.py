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

