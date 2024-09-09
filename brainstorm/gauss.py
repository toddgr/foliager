"""
File: gauss.py
Author: Grace Todd
Date: September 9, 2024
Description: A Gaussian randomization function to create smoother looking averages. 
            Adapted from C++ code provided by Mike Bailey.
"""

import math
import random

# Define constants
F_PI = math.pi
F_2_PI = 2.0 * F_PI
F_PI_2 = F_PI / 2.0


def Gaussian(mean, stddev):
    while True:
        numsigma = Ranf(-3.0, 3.0)
        p = math.exp(-numsigma * numsigma / 2.0) / math.sqrt(F_2_PI)
        level = Ranf(0.0, 1.0 / math.sqrt(F_2_PI))

        if p >= level:
            break

    return mean + numsigma * stddev


def Ranf(low, high):
    return low + (high - low) * random.random()


def Ranf_int(ilow, ihigh):
    low = float(ilow)
    high = float(ihigh) + 0.9999
    return int(Ranf(low, high))


if __name__ == "__main__":
    # example usage
    AVG = 7.0
    STDDEV = 2.0
    for i in range(10000):
        v = Gaussian(AVG, STDDEV)
        print(f"{v:8.3f}")
