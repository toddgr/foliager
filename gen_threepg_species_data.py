import csv
from datetime import datetime
from parse_tree_input import csv_file_to_list

gen_file = "generated_species_data.py"
csv_file = "Parameters/default_species_data.csv"

def create_header():
    """ 
        Creates the description of the tree class file.
    """
    file_name = 'File name: ' + gen_file + '\n'
    author = 'Author: Grace Todd\n'
    # Get today's date
    current_date = datetime.now().date()
    # Format the date as a string
    date_string = current_date.strftime("%B %d, %Y")
    todays_date = "Date: " + date_string + "\n"
    description = "Description: " + "Holds the SpeciesData class, which will be used to manipulate common parameters\n\tfor each of the species used in a simulation.\n"
    
    header = '\"\"\"\n' + file_name + author + todays_date + description + '\"\"\"\n'
    return header

def generate_python_file(csv_file_path, output_file_path):
    with open(csv_file_path, 'r') as file:
        # Read the header to get the attribute names
        header = next(csv.reader(file))
    
    with open(output_file_path, 'w') as output_file:
        output_file.write(create_header())
        output_file.write("\nfrom parse_tree_input import csv_file_to_list\n\n")
        output_file.write("class SpeciesData:\n")
        output_file.write("    def __init__(self, " + ", ".join(header) + "):\n")
        output_file.write("        \"\"\"\n")
        output_file.write("        Initializes the SpeciesData class with the provided attributes.\n")
        output_file.write("        \"\"\"\n")
        
        for attribute in header:
            output_file.write(f"        self.{attribute} = {attribute}\n")
        
        output_file.write("\n    def print_species_data(self):\n")
        output_file.write("        \"\"\"\n")
        output_file.write("        Prints all attributes of the SpeciesData instance.\n")
        output_file.write("        \"\"\"\n")
        output_file.write("        for attr, value in vars(self).items():\n")
        output_file.write("            print(f\"{attr}: {value}\")\n\n")

        output_file.write("def parse_species_data(file_path):\n")
        output_file.write("    species_list = csv_file_to_list(file_path)\n")
        output_file.write("    species_data_list = []\n\n")
        
        output_file.write("    for tree_data in species_list:\n")
        output_file.write("        species_instance = SpeciesData(*tree_data)\n")
        output_file.write("        species_data_list.append(species_instance)\n\n")
        
        output_file.write("    return species_data_list\n\n")

        output_file.write("# Example usage:\n")
        output_file.write("species = parse_species_data(\"your_species_data.csv\")\n")
        output_file.write("for tree in species:\n")
        output_file.write("    tree.print_species_data()\n")

# Example usage:
generate_python_file(csv_file, gen_file)
