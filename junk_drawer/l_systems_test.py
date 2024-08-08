"""
File: l_systems_test.py
Author: Grace Todd
Date: August 8, 2024
Description: A sandbox for creating an l systems class that allows for
            procedural tree generation.
"""


def generate_l_system(n, d, axiom, rules):
    """
        n = number of iterations
        d = degrees
        axiom = the initial string
        rules = dict of production rules
    """

    # Rewrite the string for every iteration
    string = axiom

    for _ in range(n):
        string = ''
        print(f'starting string: {axiom}')

        # apply production rules
        for char in axiom:
            if char in rules:
                string += rules[char]
            else:
                string += char

    print(f'final string: {string}')


    # Interpret each instruction into coordinates and edges
    pass


if __name__ == '__main__':
    # test - generating a quadratic koch island
    n = 1
    d = 90
    axiom = 'F-F-F-F'
    rules = {'F':'FF-F-F-F-F-F+F'}

    generate_l_system(n, d, axiom, rules)