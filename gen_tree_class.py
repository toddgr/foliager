"""
File: gen_tree_class.py
Author: Grace Todd
Date: January 19, 2024
Description: Generates tree class and ensures that the tree class updates with new attributes provided in default_tree_chart.csv.
            Takes in the attributes from default_tree_chart, ensures that the tree class has the correct attributes and 
            corresponding functions. If not, modifies tree_class
"""

from datetime import datetime
tree_class_file_name = "tree_class_test.py"

def create_header():
    file_name = 'File name: tree_class_test.py\n'
    author = 'Author: Grace Todd\n'
    # Get today's date
    current_date = datetime.now().date()
    # Format the date as a string
    date_string = current_date.strftime("%Y-%m-%d")
    todays_date = "Date: " + date_string + "\n"
    description = "Tree class. Holds information on a given tree type, derives information on each tree by parsing an input file.\n\
            Currently only derives name, but will be able to hold more attributes in the future.\n"
    
    header = '\"\"\"\n' + file_name + author + todays_date + description + '\"\"\"\n'
    return header

if __name__ == '__main__':
    with open(tree_class_file_name, 'w') as file:
        # Create header
        file.write(
            create_header()
        )

