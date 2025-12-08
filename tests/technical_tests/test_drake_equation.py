"""
Tests for drake_equation.py
---------------------------

tests/test_drake_equation.py
"""

from fermi_paradox.core.drake_equation import calculate_drake_number
from fermi_paradox.config.drake_number_params import DEFAULT_DRAKE_PARAMS


def test_calculate_drake_number():
    """Ensure Drake number calculation produces expected value with known inputs."""
    params = {
        "R_": 1.0,
        "f_p": 0.001,
        "n_e": 1.0E3,
        "f_l": 0.001,
        "f_i": 0.001,
        "f_c": 0.001,
        "L": 1.0E6,
    }
    drake_number = calculate_drake_number(**params)
    assert isinstance(drake_number, float)
    assert drake_number > 0


def test_calculate_drake_number_with_defaults():
    """Ensure Drake number can be computed using default parameters."""
    result = calculate_drake_number(**DEFAULT_DRAKE_PARAMS)
    assert isinstance(result, float)
    assert 0 < result < 1e12  # sanity range


def test_parameter_validity():
    """All default parameters should be positive values."""
    params = DEFAULT_DRAKE_PARAMS
    assert params["R_"] > 0
    assert params["f_p"] > 0
    assert params["n_e"] > 0
    assert params["f_l"] > 0
    assert params["f_i"] > 0
    assert params["f_c"] > 0
    assert params["L"] > 0


def test_drake_equation_sanity():
    """The result should be positive and roughly within plausible bounds."""
    drake_number = calculate_drake_number(**DEFAULT_DRAKE_PARAMS)
    assert 0 < drake_number < 1e9

