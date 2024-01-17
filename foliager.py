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


def ask_nlp(prompt, model="gpt-3.5-turbo"):
    # Ask ChatGPT a question, return the answer.
    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0)

    return response.choices[0].message.content   

def make_valid_filename(input_string):
    # Remove any characters that are not alphanumeric, underscores, or hyphens
    cleaned_string = re.sub(r'[^a-zA-Z0-9_-]', '_', input_string)

    # Remove leading and trailing underscores and hyphens
    cleaned_string = cleaned_string.strip('_-')

    # Ensure the file name is not empty
    if not cleaned_string:
        cleaned_string = 'untitled'

    # Limit the length of the file name to a reasonable size (adjust as needed)
    max_length = 255
    cleaned_string = cleaned_string[:max_length]

    return cleaned_string + "_Foliage.txt"


prompt = "Give a list of foliage types that can be found in "
location = input("Enter the climate, city, or area:")
prompt += location
print(prompt)

#response = ask_nlp(prompt) #commented out to save query time
#print(response)

response = "1. Douglas Fir\n2. Western Hemlock"
foliage_file = make_valid_filename(location)

print("foliage filename:", foliage_file)

# with open(foliage_file, 'w') as file:
#     # Write the string to the file
#     file.write(response)
