from flask import render_template, flash, current_app, redirect, url_for, request, abort
from flask_login import login_required, current_user

from app.auth.models import User
from app.weather import weather
from app.weather.forms import CityForm
from app.weather.models import Country, UserCity, City
from utils.ip.get_current_city import main as get_current_city
from utils.weather.city_weather import main as get_weather


@weather.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = CityForm()
    city_name = get_current_city()
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
        if not country:
            flash('Country not found')
            return redirect('weather.index')

    return render_template('weather/get_weather.html',
                           title='Get city',
                           form=form,
                           city_name=city_name,
                           city_weather=city_weather,
                           country=country)


@weather.route('/city/add', methods=['POST'])
@login_required
def add_city():
    city_name = request.form.get('city').capitalize()

    city = City.select().where(City.name == city_name).first()
    if not city:
        country = request.form.get('country')
        city = City(
            name=city_name,
            country=country)
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
    user_cities = (
        UserCity
        .select(City)
        .join(User)
        .switch(UserCity)
        .join(City)
        .where(UserCity.user == current_user)
        .order_by(City.name)
    )

    country_name = request.args.get('country')
    if country_name:
        user_cities = [user_city for user_city in user_cities if user_city.city.country.name == country_name]

    return render_template(
        'weather/show_user_cities.html',
        title=f'Cities of {current_user.username}',
        cities=user_cities)


@weather.route('/add/city/<string:city_name>', methods=['GET', 'POST'])
@login_required
def show_city_detail(city_name):
    """Show user city information"""

    api_key = current_app.config['WEATHER_API_KEY']
    city_name = city_name.capitalize()

    user_city = (
        UserCity
        .select(City)
        .join(User)
        .where(User.id == current_user.id)
        .switch(UserCity)
        .join(City)
        .where(City.name == city_name).first()
    )

    if not user_city:
        abort(404)

    city_weather = get_weather(user_city.city.name, api_key)
    if 'message' in city_weather:
        flash(city_weather['message'])
        return redirect(url_for('.index'))

    return render_template(
        'weather/show_user_city_detail.html',
        title=f'Weather info about {user_city.city.name}',
        city_weather=city_weather,
        country=user_city.city.country)


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
