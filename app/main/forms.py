from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired


class GenerateDataForm(FlaskForm):
    qty = SelectField(
        'Quantity',
        validators=[DataRequired()],
        choices=[10, 15, 25]
    )
    submit = SubmitField('Generate users')


