"""
File: foliager.py
Author: Grace Todd
Date: January 17, 2024
Description: Uses ChatGPT to derive a list of foliage from an area specified by the user.
"""

from openai import OpenAI

client = OpenAI(api_key='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')

import os

import pandas as pd

import time


def get_completion(prompt, model="gpt-3.5-turbo"):

    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(model=model, messages=messages, temperature=0)

    return response.choices[0].message.content   

prompt = "What kinds of trees can you find in the high desert?"

response = get_completion(prompt)

print(response)