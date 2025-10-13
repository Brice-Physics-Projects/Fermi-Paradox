"""
API routes for Fermi Paradox application.

src/fermi_paradox/api/routes.py
"""

from flask import Blueprint, render_template, jsonify
from fermi_paradox.core.drake_equation import DRAKE_NUMBER

api_bp = Blueprint("api", __name__)

@api_bp.route("/")
def home():
    """Render homepage with Drake number summary."""
    return render_template("index.html", drake_number=DRAKE_NUMBER)

@api_bp.route("/api/drake")
def get_drake_number():
    """Return Drake number as JSON."""
    return jsonify({"drake_number": DRAKE_NUMBER})
