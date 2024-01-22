"""
File: tree_creator.py
Author: Grace Todd
Date: January 19, 2024
Description: A brainstorm for future implementation of trees. Functions that would help to create tree assets
            using a mix-and-match formula. There's a lot of work that needs to be done before this can be
            implemented.
"""

def merge_obj_files(file1_path, file2_path, output_path):
    # Read data from the first OBJ file
    with open(file1_path, 'r') as file1:
        obj1_lines = file1.readlines()

    # Read data from the second OBJ file
    with open(file2_path, 'r') as file2:
        obj2_lines = file2.readlines()

    # Combine vertices and faces from both files
    combined_lines = obj1_lines + obj2_lines

    # Write the combined data to the output file
    with open(output_path, 'w') as output_file:
        output_file.writelines(combined_lines)

    print(f'Merged OBJ files: {file1_path} and {file2_path}. Output saved to: {output_path}')

# Example usage
# file1_path = 'path/to/first/file.obj'
# file2_path = 'path/to/second/file.obj'
# output_path = 'path/to/output/merged_file.obj'

# merge_obj_files(file1_path, file2_path, output_path)
