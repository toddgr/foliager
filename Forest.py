import random
from Species import Species
import csv 

class Forest:
    """
    Holds information about the environment, climate, and collection of trees found in the forest.
    Also might store a list of species found in the environment
    """
    def __init__(self, climate, species, num_trees=1, t=12):
        """
        Input: A list of climate conditions for each month of the year
        Attributes:
            - Climate : [ClimateByMonth]
            - Trees : [Tree]
        """
        # create climate list
        self.climate_list = self.read_climate_data(climate)
        self.t = t # number of months in the simulation

        # initialize list of trees
        self.trees_list = []
        self.num_trees = num_trees

        # create species list
        self.species_list = self.create_species_list(species)


    def read_climate_data(self, climate_filepath):
        """
        Input: Climate CSV file
        Output: A list of 12 ClimateByMonth instances, one for each month.

        TODO I'm separating this out so that in the future I can easily change the
        climate input -- CSV implementation is temporary
        """

        climate_csv = self.read_csv(climate_filepath)
        climate_data = []

        for month in climate_csv:
            month_instance = self.ClimateByMonth(*month)
            climate_data.append(month_instance)

        return climate_data


    def create_species_list(self, species_file):
        """
        Input: Species CSV filepath
        Output: A list of Species class instances, one for each species of tree.
        """
        # convert CSV to list
        species_csv = self.read_csv(species_file)

        # Create a new Species instance for each listed species
        species_list = []
        for species in species_csv:
            species_instance = Species(*species)
            species_list.append(species_instance)
        return species_list


    def read_csv(self, filepath):
        """
        Input: CSV file for either species or climate
        Output: A list of all information in the CSV
        """
        data_list = []
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader) # skip the header row
            for row in reader:
                # Exclude lines starting with a comment character (e.g., #)
                if not row or row[0].startswith("#"):
                    continue
                data_list.append(row)
        return data_list


    def add_tree(self, tree):
        """ 
        Adds a Tree object to the forest's list of trees.
        """
        self.trees_list.append(tree)


    def print_tree_list(self):
        print("======= LIST OF TREES IN THIS FOREST: =======")
        for tree in self.trees_list:
            print(f'{tree.key}: {tree.position}')


    def get_climate(self):
        """
        Prints a list of climate information for each month.
        """
        print("========== GETTING CLIMATE FOR THIS FOREST ==========")
        print("month, tmax (C), tmin (C), rain (cm), solar radiation (kwh/m2), num frost days,\
 soil water (cm/ft), max soil water (cm/ft), soil texture")
        for month in self.climate_list:
            print(f'{month.month}, {month.tmax}, {month.tmin}, {month.rain}, {month.solar_rad},\
 {month.frost_days}, {month.soil_water}, {month.max_soil_water}, {month.soil_texture}')


    def compute_competition_indices(self):
        """
        Calculates the competition index for each tree in the forest using the BAL theorem.
        """

        # Sort the list of trees by basal area (smallest to largest)
        # That way the competition index calculation can be quick and easy

        total_basal_area = sum(tree.ba for tree in self.trees_list)
        basal_area_list = sorted(self.trees_list, key=lambda tree: tree.ba)
        
        # get the sum of the basal area for all the trees greater than the current tree
        i = 1
        for tree in self.trees_list:
            greater_tree_sum = sum(tree.ba for tree in basal_area_list[i:]) # IF index is greater than tree in basal_area_list 
            tree.c = greater_tree_sum / total_basal_area
            i+=1


    class ClimateByMonth:
        """
        A class that holds information on the climate for one month of the year.
        A ClimateByMonth instance is initialized for each month of the year.
        """
        def __init__(self, month:str, tmax:int, tmin:int, r:float, sr:float, fd:int, st:str, vpd:float):
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
                - vpd: float
            """
            self.month = month          # January, February, etc.
            self.tmax = int(tmax)       # Average maximum temperature (celsius)
            self.tmin = int(tmin)       # Average minimum temperature (celsius)
            self.rain = float(r)        # Average rainfall (cm)
            self.solar_rad = float(sr)         # Average solar radiation (kwh/m2)
            self.frost_days = int(fd)        # Average number of frost days (int)
            self.soil_texture = st
            self.vpd = float(vpd)

            self.soil_water, self.max_soil_water = self.estimate_soil_water(st)


        def estimate_soil_water(self, soil_texture):
            """
            Uses soil texture input to estimate soil water.

            LLM categorizes the type of soil for the area,
            and we approximate its values based on the category
            data from https://ucanr.edu/sites/UrbanHort/files/80243.pdf
            and converted to metric units from in. per ft. of soil
            to cm per ft. of soil

            |-----------------------------------------------|
            | === soil texture ===  | holding capacity (cm) |
            |-----------------------|-----------------------|
            | very coarse sand      | 1.016 - 1.905         |   A
            |-----------------------|-----------------------|
            | coarse sand           |                       |
            | fine sand             | 1.905 - 3.175         |   B
            | loamy sand            |                       |
            |-----------------------|-----------------------|
            | sandy loams           |                       |   C
            | fine sandy loams      | 3.175 - 4.445         |
            |-----------------------|-----------------------|
            | very fine sandy loams |                       |
            | loams                 | 3.81 - 5.842          |   D
            | silt loams            |                       |
            |-----------------------|-----------------------|
            | clay loams            |                       |
            | silt clay loams       | 4.445 - 6.35          |   E
            | sandy clay loams      |                       |
            |-----------------------|-----------------------|
            | sandy clays           |                       |
            | silty clays           | 4.064 - 6.35          |   F
            | clays                 |                       |
            |-----------------------------------------------|
            """
            # Holding capacity A
            if soil_texture == "very_coarse_sand":
                # capacity range
                soil_min = 1.016
                soil_max = 1.905

            # Holding capacity B
            elif soil_texture in ("coarse_sand", "fine_sand", "loamy_sand"):
                # capacity range - lowest in B
                soil_min = 1.905
                soil_max = 3.175
                # TODO refine the categories and apply different
                # sections for each subcategory
                #max = ((max - min) / 3) + min

            # Holding capacity C
            elif soil_texture in ("sandy_loams", "fine_sandy_loams"):
                soil_min = 3.175
                soil_max = 4.445

            # Holding capacity D
            elif soil_texture in ("very_fine_sandy_loams", "loams", "silt_loams"):
                soil_min = 3.81
                soil_max = 5.842

            # Holding capacity E
            elif soil_texture in ("clay_loams", "silt_clay_loams", "sandy_clay_loams"):
                soil_min = 4.445
                soil_max = 6.35

            # Holding capacity F
            elif soil_texture in ("sandy_clays", "silty_clays", "clays"):
                soil_min = 4.064
                soil_max = 6.35

            else:
                print(f"ERROR Invalid soil texture: {soil_texture}")
                return None

            soil_water = random.uniform(soil_min,soil_max)
            max_soil_water = soil_max
            return soil_water, max_soil_water


        def get_month_climate(self):
            """
            Prints this month's climate data.
            """
            print(f'============ Climate data for {self.month} ============')
            print(f'Temperature: between {self.tmin} and {self.tmax} degrees Celsius.')
            print(f'Average rainfall: {self.rain} days this month.')
            print(f'Solar radiation: about {self.solar_rad} kwh/m2.')
            print(f'Frost days: {self.frost_days} this month.')
            print(f'Soil: {self.soil_texture}, around {self.soil_water} cm/ft of water \
with a maximum of {self.max_soil_water} cm/ft.')
