from flask import Blueprint

weather = Blueprint('weather', __name__, url_prefix='/weather')

from app.weather import routes
