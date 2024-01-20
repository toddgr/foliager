"""
File: foliager.py
Author: Grace Todd
Date: January 17, 2024
Description: Uses ChatGPT to derive a list of foliage from an area specified by the user.
    OpenAI Documentation: https://platform.openai.com/docs/overview
"""

from openai import OpenAI
client = OpenAI(api_key='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')

import os
import pandas as pd
import time
import re

#from tree_class import parse_tree_file, Tree


def ask_nlp(prompt, model="gpt-3.5-turbo"):
    # Ask ChatGPT a question, return the answer.
    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0)

    return response.choices[0].message.content   

def make_valid_filename(input_string):
    extension = "_foliage.csv"
    cleaned_string = re.sub(r'[^\w\s-]', '', input_string)  # Remove special characters except for spaces and hyphens
    cleaned_string = re.sub(r'\s+', '_', cleaned_string)    # Replace consecutive spaces with a single underscore
    cleaned_string = cleaned_string.strip('_-')

    if not cleaned_string:
        cleaned_string = 'untitled'

    max_length = 255 - len(extension)
    cleaned_string = cleaned_string[:max_length]

    return cleaned_string + extension

if __name__ == '__main__':
    prompt = "Give an unnumbered list of foliage types in CSV format that can be found in "
    location = input("Enter the climate, city, or area:")
    prompt += location
    attributes = " with the following attributes: Name, Growth Rate, Average Lifespan" # Make this dynamic
    prompt += attributes
    print(prompt)
    print("Generating foliage list for ", location, "...")

    # response = ask_nlp(prompt) #commented out to save query time
    # print(response)

    test_response = "Name,              Growth Rate,    Average Lifespan\n \
                    Douglas Fir,        Medium,         500 years\n \
                    Western Red Cedar,  Medium,         500 years \
                    Bigleaf Maple,      Medium,         100 years"
    foliage_file = make_valid_filename(location)

    with open(foliage_file, 'w') as file:
        # Write the string to the file
        file.write(test_response)
        print("Writing to file ", foliage_file)

    #foliage_list = parse_tree_file(foliage_file)

