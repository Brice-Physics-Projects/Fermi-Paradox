"""
Internal development testing

src/fermi_paradox/main.py
"""

from fermi_paradox import create_app

def start_app():
    """Start the Flask app (used for debugging or CLI calls)."""
    app = create_app()
    app.run(debug=True)

if __name__ == "__main__":
    start_app()






"""
Archived calculations
---------------------

pi = np.pi
galactic_disc_height = 1000 # LY
galactic_disc_area = 7.85 * 10**9 # SQ. LY
R_galactic_disc_radius = galactic_disc_area / galactic_disc_height/2
radio_bubble_volume_est = 4.19 * 10**6 # CU. LY
radio_bubble_radius = 200 / 2 # LY

galactic_disc_volume = pi * R_galactic_disc_radius**2 * galactic_disc_height # CU. LY
radio_bubble_volume_calc = 4/3 * pi * radio_bubble_radius**3 # CU. LY


print(f"{R_galactic_disc_radius: ,.2f}")
"""

if __name__ == "__main__":
    start_app()
