from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api/v1')

from app.api import authentification
from app.api.weather import countries, cities
