from flask import render_template, flash, current_app, redirect, url_for, request, abort
from flask_login import login_required, current_user

from app.auth.models import User
from app.weather import weather
from app.weather.forms import CityForm
from app.weather.models import Country, UserCity, City
from utils.weather.city_weather import main as get_weather


@weather.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = CityForm()
    city_name = None
    city_weather = None
    country = None

    if form.validate_on_submit():
        api_key = current_app.config['WEATHER_API_KEY']
        city_name = form.city_name.data
        city_weather = get_weather(city_name, api_key)

        if 'message' in city_weather:
            flash(city_weather['message'], 'danger')
            return redirect(url_for('weather.index'))

        country = Country.select().where(Country.code == city_weather['country']).first()

    return render_template('weather/get_weather.html',
                           title='Get city',
                           form=form,
                           city_name=city_name,
                           city_weather=city_weather,
                           country=country)


@weather.route('/add/city/<string:city_name>, <string:country_id>', methods=['POST'])
@login_required
def add_city(city_name, country_id):
    city_name = city_name.capitalize()

    city = City.select().where(City.name == city_name).first()
    if not city:
        city = City(
            name=city_name,
            country=country_id
        )
        city.save()

    city_user = UserCity.select().where(UserCity.city == city).first()
    if not city_user:
        city_user = UserCity(city=city.id,
                             user=current_user.id)
        city_user.save()

        flash(f"City '{city_name}' added to tracking.", 'success')
    else:
        flash(f"You have already added this city before.", 'info')
    return redirect(url_for('weather.index'))


@weather.route('/show_user_cities')
@login_required
def show_user_cities():
    """Show user city information"""

    username = current_user.username
    user = User.select().where(User.username == username).first()
    if not user:
        abort(404)

    cities = UserCity.select().where(UserCity.user == user)

    return render_template('weather/show_user_cities.html',
                           title='Show user cities',
                           cities=cities)


@weather.route('/delete/cities', methods=['POST'])
@login_required
def delete_cities():
    """Delete selected cities"""

    selectors = list(map(int, request.form.getlist('selectors')))

    if not selectors:
        flash('Nothing to delete', 'warning')
        return redirect(url_for('weather.show_user_cities'))

    message = 'Deleted: '
    for selector in selectors:
        city = UserCity.get(UserCity.city == int(selector))
        message += f'{city.city.name} '
        city.delete_instance()
    flash(message, 'info')
    return redirect(url_for('weather.show_user_cities'))


@weather.route('/add/city/<string:city_name>', methods=['GET', 'POST'])
@login_required
def show_city(city_name):
    """Show user city information"""

    api_key = current_app.config['WEATHER_API_KEY']
    city_weather = get_weather(city_name, api_key)

    if 'message' in city_weather:
        flash(city_weather['message'], 'danger')
        return redirect(url_for('weather.index'))

    country = Country.select().where(Country.code == city_weather['country']).first()

    return render_template('weather/show_city.html',
                           title='Show user cities',
                           city_name=city_name,
                           city_weather=city_weather,
                           country=country)

