
from threepg_species_data import SpeciesData
import csv

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
    #print(f"tree_params: {tree_params}")

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