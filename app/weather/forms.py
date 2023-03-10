from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp


class CityForm(FlaskForm):
    city_name = StringField('City e.g. Barcelona, Tokyo, New York, Las Vegas, London...',
                            validators=[DataRequired(), Length(2, 100),
                                        Regexp('[a-zA-Z]', 0, 'City name must have only letters')],
                            render_kw={'placeholder': 'Enter city'})
    submit = SubmitField('Show',
                         render_kw={'class': 'btn btn-success', 'id': "Show"})

    # def validate_city_name(self, city_name):
    #     """validate_ 'city_name' must match with city_name!!! """
    #
    #     if UserCity.select().where(UserCity.city_name == city_name.data).first():
    #         raise ValidationError('This city you have already added')
    #
    #     if not city_name.data in valid_cities:
    #         raise ValidationError('City not found, please try again')
