from flask import jsonify, abort, request, url_for
from flask_paginate import Pagination

from app.api import api
from app.weather.models import Country, City


@api.route('/countries/', methods=['GET'])
def get_countries():
    per_page = 10
    page = request.args.get('page', 1, type=int)
    total = Country.select().count()

    pagination = Pagination(page=page, per_page=per_page, total=total, record_name='countries')
    prev_page = None
    next_page = None

    if pagination.has_prev:
        prev_page = url_for('api.get_countries', page=page - 1)
    if pagination.has_next:
        next_page = url_for('api.get_countries', page=page + 1)

    countries = Country.select().paginate(page, per_page)
    response = [country.to_json() for country in countries]
    return jsonify({
        'countries': response,
        'prev_page': prev_page,
        'next_page': next_page,
        'total': total
    }), 200


@api.route('/countries/<int:country_id>', methods=['GET'])
def get_country(country_id):
    country = Country.select().where(Country.id == country_id).first()
    if not country:
        abort(404)
    return jsonify(country.to_json()), 200


@api.route('/countries/<int:country_id>/cities/', methods=['GET'])
def get_country_cities(country_id):
    country = Country.select().where(Country.id == country_id).first()
    if not country:
        abort(404)

    per_page = 10
    page = request.args.get('page', 1, type=int)
    total = City.select().count()

    pagination = Pagination(page=page, per_page=per_page, total=total, record_name='cities')
    prev_page = None
    next_page = None

    if pagination.has_prev:
        prev_page = url_for('api.get_country_cities', country_id=country_id, page=page - 1)
    if pagination.has_next:
        next_page = url_for('api.get_country_cities', country_id=country_id, page=page + 1)

    cities = City.select().where(City.country == country).paginate(page, per_page)
    response = [city.to_json() for city in cities]

    return jsonify({
        'cities': response,
        'prev_page': prev_page,
        'next_page': next_page,
        'total': total}), 200


@api.route('/countries/<int:country_id>/cities/<int:city_id>', methods=['GET'])
def get_country_city(country_id, city_id):
    country = Country.select().where(Country.id == country_id).first()
    if not country:
        abort(404)

    city = City.select().where((City.country == country) & (City.id == city_id)).first()
    if not city:
        abort(404)
    return jsonify(city.to_json()), 200
