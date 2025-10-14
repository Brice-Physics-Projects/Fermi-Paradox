"""
API routes for Fermi Paradox application.

src/fermi_paradox/api/routes.py
"""

from flask import Blueprint, render_template, request
from fermi_paradox.config.drake_number_params import DEFAULT_DRAKE_PARAMS
from fermi_paradox.core.drake_equation import calculate_drake_number
from fermi_paradox.api.forms import DrakeForm

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
    DRAKE_NUMBER = calculate_drake_number(**params)
    return render_template("drake.html", DRAKE_NUMBER=DRAKE_NUMBER, params=params)

@api_bp.route("/api/edit-drake", methods=["GET", "POST"])
def edit_drake_params():
    """Edit Drake parameters."""
    name = None
    # ✅ Prefill the form with your default Drake parameters
    form = DrakeForm(data={
        "R_": DEFAULT_DRAKE_PARAMS["R_"],
        "f_p": DEFAULT_DRAKE_PARAMS["f_p"],
        "n_e": DEFAULT_DRAKE_PARAMS["n_e"],
        "f_l": DEFAULT_DRAKE_PARAMS["f_l"],
        "f_i": DEFAULT_DRAKE_PARAMS["f_i"],
        "f_c": DEFAULT_DRAKE_PARAMS["f_c"],
        "L": DEFAULT_DRAKE_PARAMS["L"],
    })

    if form.validate_on_submit():
        params = {
        "R_" : form.R_.data,
        "f_p" : form.f_p.data,
        "n_e" : form.n_e.data,
        "f_l" : form.f_l.data,
        "f_i" : form.f_i.data,
        "f_c" : form.f_c.data,
        "L" : form.L.data,
        }

        # loop through params
        for key, value in params.items():
            if value is None:
                params[key] = DEFAULT_DRAKE_PARAMS[key]

        # calcuate drake's number
        DRAKE_NUMBER = calculate_drake_number(**params)
        return render_template("drake.html", form=form, DRAKE_NUMBER=DRAKE_NUMBER, params=params)
    return render_template("edit-drake.html", form=form, name=name)
