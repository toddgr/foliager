import csv
from datetime import datetime
from parse_tree_input import csv_file_to_list

gen_file = "threepg_species_data.py"
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

def get_tree_names_function():
    # Only if there is a names label in there, but there SHOULD BE
    get_tree_names =  "def get_tree_names(species_data_list):\n"
    get_tree_names += "\t# returns a list of the tree names found in the species data CSV.\n"
    get_tree_names += "\ttree_names = []\n"
    get_tree_names += "\tfor tree in species_data_list:\n"
    get_tree_names += "\t\ttree_names.append(tree.name)\n"
    get_tree_names += "\treturn tree_names\n\n"
    return get_tree_names


def generate_python_file(csv_file_path, output_file_path):
    with open(csv_file_path, 'r') as file:
        # Read the header to get the attribute names
        header = next(csv.reader(file))
        parameter_init = ""
        for parameter in header:
            if parameter.startswith('q_') or parameter.startswith("name"):
                parameter_init+= parameter
            else:
                parameter_init += parameter + "=0"
            parameter_init += ", "
    
    with open(output_file_path, 'w') as output_file:
        output_file.write(create_header())
        output_file.write("\nimport csv\n\n")
        output_file.write("class SpeciesData:\n")
        output_file.write("    def __init__(self, " + parameter_init + "):\n")
        output_file.write("        \"\"\"\n")
        output_file.write("        Initializes the SpeciesData class with the provided attributes.\n")
        output_file.write("        \"\"\"\n")
        
        for attribute in header:
            if attribute.startswith('q_'):
                output_file.write(f"        self.{attribute} = {attribute}.split('/')\n")
            elif attribute.startswith('name'):
                output_file.write(f"        self.{attribute} = {attribute}\n")
            else:
                output_file.write(f"        self.{attribute} = float({attribute})\n")
        
        output_file.write("\n    def print_species_data(self):\n")
        output_file.write("        \"\"\"\n")
        output_file.write("        Prints all attributes of the SpeciesData instance.\n")
        output_file.write("        \"\"\"\n")
        output_file.write("        for attr, value in vars(self).items():\n")
        output_file.write("            print(f\"{attr}: {value}\")\n\n")

        output_file.write("""\n    def get_species_info(self):
        \"\"\"
        Writes all attributes of the SpeciesData instance as a list.
        \"\"\"
        tree_info = \"\"
        for attr, value in vars(self).items():
            str_value = str(value)
            if '[' in str_value or ']' in str_value:
            # if the value is a list of things
                parts = [part.strip(\"[] '\") for part in str_value.split(\",\")]
                result = \"/\".join(parts)
                tree_info += result + \",\"
            else:
                tree_info += str_value + \",\"
        
        tree_info += \"\"\n
        return tree_info\n\n""")
        output_file.write(get_tree_names_function())

        output_file.write("def parse_species_data(file_path):\n")
        output_file.write("    species_list = csv_file_to_list(file_path)\n")
        output_file.write("    species_data_list = []\n\n")
        
        output_file.write("    for tree_data in species_list:\n")
        output_file.write("        species_instance = SpeciesData(*tree_data)\n")
        output_file.write("        species_data_list.append(species_instance)\n\n")
        
        output_file.write("    return species_data_list\n\n")

        output_file.write('''
def parse_csv_file(file_path):
    # Parses a CSV file output from NLP into Tree and TreeList objects # Needs to be updated as more attributes for trees are included
    # Common_name,scientific_name,leaf_shape_(oval/truncate/elliptical/lancolate/linear/other),
    #canopy_density_(very_thin/thin/medium/dense/very_dense),deciduous_or_evergreen,
    #leaf_color_(green),tree_form_(round/spreading/pyramidal/oval/conical/vase/columnar/open/weeping/irregular),
    #tree_roots_(deep/shallow),habitat_(polar/temperate/dry/continental/tropical/subtropical/subcontinental/
    #mediterranean/alpine/arid/subarctic/subalpine),bark_texture_(smooth/lenticels/furrows/ridges/cracks/scales/strips),
    #bark_color_(gray/white/red/brown)
    trees = []
    # read in the tree params
    tree_params = csv_file_to_list(file_path)
    print(f"tree_params: {tree_params}")

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # read in the tree_params and assign the value at row[param] for param in tree_params
            name = row['Common_name']
            name_scientific = row['scientific_name']
            leaf_shape = row['leaf_shape_(oval/truncate/elliptical/lancolate/linear/other)']
            canopy_density = row['canopy_density_(very_thin/thin/medium/dense/very_dense)']
            deciduous_evergreen = row['deciduous_or_evergreen']
            leaf_color = row['leaf_color_(green)']
            tree_form= row['tree_form_(round/spreading/pyramidal/oval/conical/vase/columnar/open/weeping/irregular)']
            tree_roots = row['tree_roots_(deep/shallow)']
            habitat = row['habitat_(polar/temperate/dry/continental/tropical/subtropical/subcontinental/mediterranean/alpine/arid/subarctic/subalpine)']
            bark_texture = row['bark_texture_(smooth/lenticels/furrows/ridges/cracks/scales/strips)']
            bark_color = row['bark_color_(gray/white/red/brown)']
            tree = SpeciesData(name, name_scientific, leaf_shape, canopy_density, deciduous_evergreen, leaf_color, tree_form, tree_roots, habitat, bark_texture, bark_color)
            trees.append(tree)

    return trees
''')

        output_file.write('''
def csv_file_to_list(file_path):
    attribute_list = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Exclude lines starting with a comment character (e.g., #)
            if not row or row[0].startswith("#"):
                continue
            attribute_list.append(row)
    return attribute_list
''')

        output_file.write("# Example usage:\n")
        output_file.write("#species_csv = \"test_data/douglas_fir_species_data.csv\"\n")
        output_file.write(f"#species = parse_species_data(species_csv)\n")
        output_file.write("#for tree in species:\n")
        output_file.write("    #tree.print_species_data()\n")

# Example usage:
generate_python_file(csv_file, gen_file)
