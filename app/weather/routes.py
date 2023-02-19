from flask import render_template, flash, current_app, request, redirect, url_for
from flask_login import login_required, current_user
from flask_paginate import get_page_args, Pagination

from app.auth.utils import get_quantity
from app.weather import weather
from app.weather.forms import CityForm
from app.weather.models import UserCity


@weather.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = CityForm()

    if form.validate_on_submit():
        user_city = UserCity(city_name=form.city_name.data,
                             user=current_user.id)
        user_city.save()

        flash(f"City '{form.city_name.data}' added to tracking", 'success')

    return render_template('weather/index.html',
                           title='Add City',
                           form=form)


@weather.route('/show_user_cities')
@login_required
def show_user_cities():
    """Show user city information"""

    cities = UserCity.select()
    total = cities.count()

    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    pagination_cities = get_quantity(cities,
                                     offset=offset,
                                     per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    from app.weather.weather_api import get_weather

    api_key = current_app.config['WEATHER_API_KEY']
    weather_url = current_app.config['OPENWEATHER_API_URL']

    return render_template('weather/show_user_cities.html',
                           title='Show user cities',
                           cities=pagination_cities,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           get_weather=get_weather,
                           weather_url=weather_url,
                           api_key=api_key)

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

        city = UserCity.get(UserCity.id == selector)
        message += f'{city.city_name} '
        city.delete_instance()
    flash(message, 'info')
    return redirect(url_for('weather.show_user_cities'))
