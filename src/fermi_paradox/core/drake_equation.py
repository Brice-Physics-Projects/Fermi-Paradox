"""
Core application to calculate Drakes Number

src/fermi_paradox/core/drake_equation.py
"""

import numpy as np
import math


# *************** CONSTANTS *********************

L_1961 = 50E6
L_2017 = 15.6E6
L_weighted_avg = (.2*L_1961 + .8*L_2017) / 2 #weighted average using 80% on recent data


R_ = 2 # R^*
f_p = 0.8
n_e = 0.2
f_l = 0.5
f_i = 1
f_c = 0.1
L = 1000



# CALCULATION OF DRAKE'S NUMBER

DRAKE_NUMBER = R_ * f_p * n_e * f_l * f_i * f_c * L 

print(f"Drake's Number: {DRAKE_NUMBER: ,.0f}")

def drakes_number():
    """Returns the calculated Drake's Number"""

    return DRAKE_NUMBER
