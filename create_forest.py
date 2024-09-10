"""
File: create_forest.py
Author: Grace Todd
Date: September 10, 2024
Description: Uses 3-PG to calculate various parameters of a tree, which will be used to generate
             each tree in the simulation at every time interval.
             
             Based on real, scientific data, and uses C++ skeleton framework provided by Allison
             Thompson in her thesis here: https://ir.library.oregonstate.edu/concern/honors_college_theses/x920g532g.

             A revised version of 3pg.py

             THE GENERAL IDEA:
             1. Initialize an empty forest
             2. Compute the data for each species of tree found in the forest
             3. Create individual trees from species data & plot them within the forest
             4. Compute spawned/killed trees throughout the simulation
             5. Take the final state of the forest and write to Blender
"""

