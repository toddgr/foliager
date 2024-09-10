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

import csv

"""
=====================================================================
                                CLASSES
=====================================================================
"""

class Forest:
    """
    Holds information about the environment, climate, and collection of trees found in the forest.
    Also might store a list of species found in the environment
    """
    def __init__(self, climate_filepath):
        """
        Input: A list of climate conditions for each month of the year
        Attributes:
            - Climate : [ClimateByMonth]
            - Trees : [Tree]
        """
        # create climate list
        self.climate = self.read_climate_data(climate_filepath)

        # initialize list of trees
        self.trees = []

        pass

    def read_climate_data(self, climate_filepath):
        """
        Input: Climate CSV file
        Output: A list of 12 ClimateByMonth instances, one for each month.

        TODO I'm separating this out so that in the future I can easily change the
        climate input -- CSV implementation is temporary
        """
        climate_data = []
        with open(climate_filepath, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                climate_this_month = self.ClimateByMonth(month=row['month'], tmax=row['tmax'], tmin=row['tmin'],
                                                    rain=row['rain'], sr=row['solar_rad'],fd=row['frost_days'],
                                                    st=row['soil_texture'])
                climate_data.append(climate_this_month)
        return climate_data

    def add_tree(self, tree):
        self.trees.append(tree)

    class ClimateByMonth:
        """
        A class that holds information on the climate for one month of the year.
        A ClimateByMonth instance is initialized for each month of the year.
        """
        
        def __init__(self, month:str, tmax:int, tmin:int, r:float, sr, fd, st):
            """
            Attributes:
                - month : str
                - tmax : int
                - tmin : int
                - rain : float
                - solar_rad : float
                - frost_days : int
                - soil_texture : str
                - soil_water : float        Estimated with estimate_soil_water
                - max_soil_water : float
            """
            self.month = month          # January, February, etc.
            self.tmax = tmax            # Average maximum temperature (celsius)
            self.tmin = tmin            # Average minimum temperature (celsius)
            self.rain = r               # Average rainfall (cm)
            self.solar_rad = sr         # Average solar radiation (kwh/m2)
            self.frost_days = fd        # Average number of frost days (int)
            self.estimate_soil_water(st)
        
        def estimate_soil_water(self, soil_texture):
            """
            Uses soil texture input to estimate soil water

            TODO use approximate_soil_data() here
            """
            pass

class Species:
    """
    Holds information about a specific species.
    TODO implement 3-PG calculations here
    """
    def __init__(self):
        pass


class Tree(Species):
    """
    Holds information about each individual tree in the forest.
    Inherits information about its species
    Calculates unique dimensions on initialization
    Initialization occurs when the (x,y) coordinates are generated
    """
    def __init__(self, species, x, y):
        pass


"""
=====================================================================
                                FUNCTIONS
=====================================================================
"""

def create_forest():
    # 1. Initialize forest
    # read in the climate data
    # initialize the forest based on climate data
    
    # 2. Compute data for each species

    # 3. Create indivisual trees from species data

    # 4. Repeat for spawned/killed trees

    # 5. Write to Blender
    pass

if __name__ == '__main__':
    # example usage here
    create_forest()