"""
Module containing parameters for Drake equation calculations.

src/fermi_paradox/config/drake_number_params.py
"""

L_1961 = 50E6
L_2017 = 1.0E6
L_weighted_avg = (.2*L_1961 + .8*L_2017) / 2 # weighted average using 80% on recent data


DEFAULT_DRAKE_PARAMS = {
    "R_": 2,
    "f_p": 0.8,
    "n_e": 0.2,
    "f_l": 0.5,
    "f_i": 1,
    "f_c": 0.1,
    "L": L_weighted_avg
}

__all__ = ["DEFAULT_DRAKE_PARAMS"]
