"""
Flask-WTF form for editing Drake Equation parameters.
-----------------------------------------------------

src/fermi_paradox/api/forms/drake_form.py
"""

from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class DrakeForm(FlaskForm):
    R_ = FloatField("R* (Star Formation Rate)", validators=[DataRequired(), NumberRange(min=0)])
    f_p = FloatField("f(p) (Fraction of Stars with Planets)", validators=[DataRequired(), NumberRange(min=0, max=1)])
    n_e = FloatField("n(e) (Habitable Planets per System)", validators=[DataRequired(), NumberRange(min=0)])
    f_l = FloatField("f(l) (Fraction Where Life Appears)", validators=[DataRequired(), NumberRange(min=0, max=1)])
    f_i = FloatField("f(i) (Fraction Developing Intelligence)", validators=[DataRequired(), NumberRange(min=0, max=1)])
    f_c = FloatField("f(c) (Fraction Developing Technology)", validators=[DataRequired(), NumberRange(min=0, max=1)])
    L = FloatField("L (Lifetime of Civilization in Years)", validators=[DataRequired(), NumberRange(min=0)])

    submit = SubmitField("Recalculate")
