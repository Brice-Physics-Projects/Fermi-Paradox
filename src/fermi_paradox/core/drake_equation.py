"""
Core application to calculate Drakes Number

src/fermi_paradox/core/drake_equation.py
"""

# CALCULATION OF DRAKE'S NUMBER


print(f"Drake's Number: {DRAKE_NUMBER: ,.0f}")

def calculate_drake_number(R_, f_p, n_e, f_l, f_i, f_c, L):
    """Calulates drake's number"""
    DRAKE_NUMBER = R_ * f_p * n_e * f_l * f_i * f_c * L
    return DRAKE_NUMBER
