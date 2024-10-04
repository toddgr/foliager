"""
File name: blender_create_tree_list.py
Author: Grace Todd
Date: September 25, 2024
Description: TEMPORARY file to be used for creating fake tree data to be imported
            into the blender forest generation module.

            1. come up with a list of tree types to generate
               should all be unique shapes and sizes, doesn't have
               to make sense
            2. find the average dimensions for each tree type at a certain age
            3. create a forest class object, store the species in there
            4. plot trees with randomized dimensions
            5. For each tree, generate with geometry node script
"""

import sys
sys.path.append('C:/Users/Grace/Documents/Masters_Project/foliager/')

from Tree import Tree, plot_trees
from create_forest import *
from blender.blender_geom_trees import create_tree

if __name__ == "__main__":
    # set up the forest
    example_climate = "month,tmax,tmin,rain,solar_rad,frost_days,soil_texture,vpd\n\
January,3.5,-6.1,3.8,2.5,12,loams,1.2\n\
February,6.1,-3.9,2.5,3.0,10,loams,1.5\n\
March,10.0,0.5,2.0,4.5,8,loams,1.8\n\
April,14.5,2.5,1.5,5.5,5,loams,2.1\n\
May,19.0,5.0,1.0,6.5,2,loams,2.5\n\
June,24.0,9.0,0.5,7.5,0,loams,2.8\n\
July,30.0,12.0,0.0,8.0,0,loams,3.0\n\
August,29.5,11.5,0.0,7.8,0,loams,2.9\n\
September,24.0,7.5,0.2,6.5,1,loams,2.6\n\
October,16.0,2.0,1.5,4.5,5,loams,2.3\n\
November,8.0,-2.0,3.0,2.5,10,loams,1.9\n\
December,4.0,-5.0,4.0,2.0,12,loams,1.4"

    header = 'name, scientific_name, leaf_shape, canopy_density, deciduous_evergreen, leaf_color, tree_form, tree_roots, habitat, bark_texture, bark_color, masting_cycle, seeding_age, foliage_biomass, stem_biomass, root_biomass\n'
    ponderosa_pine = 'Ponderosa Pine, Pinus ponderosa, linear, medium, evergreen, green, conical, deep, temperate, furrows, brown, 3, 5, 1.5, 2.0, 0.5\n'
    western_red_cedar = 'Western Red Cedar, Thuja plicata, other, dense, evergreen, green, spreading, shallow, temperate, strips, brown, 4, 7, 1.2, 1.8, 0.4\n'
    quaking_aspen = 'Quaking Aspen,Populus tremuloides,oval,medium,deciduous,green,irregular,shallow,temperate,smooth,white,2,3,0.8,1.0,0.3\n'
    black_cottonwood = 'Black Cottonwood,Populus trichocarpa,oval,medium,deciduous,green,spreading,shallow,temperate,furrows,brown,3,5,1.0,1.5,0.4\n'
    sugar_maple = 'Sugar Maple,Acer saccharum,truncate,medium,deciduous,green,round,shallow,temperate,smooth,gray,4,6,1.0,1.2,0.3\n'
    douglas_fir = 'Douglas Fir,Pseudotsuga menziesii,linear,dense,evergreen,green,pyramidal,deep,temperate,furrows,brown,5,8,1.5,2.5,0.6\n'
    red_alder = 'Red Alder,Alnus rubra,oval,medium,deciduous,green,irregular,shallow,temperate,smooth,gray,2,4,0.9,1.1,0.3\n'
    lodgepole_pine = 'Lodgepole Pine,Pinus contorta,linear,thin,evergreen,green,conical,deep,temperate,furrows,brown,3,5,1.2,1.6,0.4\n'
    
    example_species = header+ponderosa_pine+western_red_cedar+quaking_aspen+black_cottonwood+sugar_maple+douglas_fir+red_alder+lodgepole_pine

    forest = Forest(example_climate, example_species, num_trees=10)

    for each_species in forest.species_list:
        each_species.get_basic_info()
    # generate "fake data" for each species
    def populate_dimensions(tree, height, dbh, lcl, c_diam):
        tree.height = height
        tree.dbh = dbh
        tree.lcl = lcl
        tree.c_diam = c_diam

    # average known values for species at 50 years old
    populate_dimensions(forest.species_list[0], 20, 0.4, 11, 7) # Ponderosa Pine
    populate_dimensions(forest.species_list[1], 20, 0.4, 8, 5) # Western Red Cedar
    populate_dimensions(forest.species_list[2], 17, 0.3, 8, 5) # Quaking Aspen
    populate_dimensions(forest.species_list[3], 32, 0.85, 17, 13) # Black Cottonwood
    populate_dimensions(forest.species_list[4], 17, 0.35, 7, 12) # Sugar Maple
    populate_dimensions(forest.species_list[5], 27, 0.45, 13, 7) # Douglas Fir
    populate_dimensions(forest.species_list[6], 30, 0.5, 15, 10) # Red Alder
    populate_dimensions(forest.species_list[7], 20, 0.10, 10, 5) # Lodgepole pine
    
    # generate some trees
    plot_trees(forest)

    # randomize values for each individual tree
    for each_tree in forest.trees_list:
        each_tree.height = each_tree.generate_from(each_tree.species.height)
        each_tree.dbh = each_tree.generate_from(each_tree.species.dbh)
        each_tree.lcl = each_tree.generate_from(each_tree.species.lcl)
        each_tree.c_diam = each_tree.generate_from(each_tree.species.c_diam)
    
    # now that we have all the data:
    for each_tree in forest.trees_list:
        create_tree(each_tree)
        pass