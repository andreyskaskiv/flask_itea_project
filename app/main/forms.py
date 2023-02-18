from flask_wtf import FlaskForm
from wtforms import SubmitField


class GenerateDataForm(FlaskForm):
    submit = SubmitField('Generate users')


