"""
API routes for Fermi Paradox application.

src/fermi_paradox/api/routes.py
"""

from flask import Blueprint, render_template, request
from fermi_paradox.config.drake_number_params import DEFAULT_DRAKE_PARAMS
from fermi_paradox.core.drake_equation import calculate_drake_number

api_bp = Blueprint("api", __name__)

@api_bp.route("/")
def home():
    """Render homepage with Drake number summary."""
    return render_template("home.html")

@api_bp.route("/api/drake", methods=["GET", "POST"])
def get_drake_number():
    """Return Drake number."""
    params = DEFAULT_DRAKE_PARAMS
    if request.method == "POST":
        for key in params.keys():
            value = request.form.get(key)
            if value:
                params[key] = float(value)
    N = calculate_drake_number(**params)
    return render_template("results.html", N=N, params=params)
