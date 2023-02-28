from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

from peewee import SqliteDatabase

from app.config import config
from app.base_model import database_proxy
from app.auth.models import Profile, Role, User, Post
from app.weather.models import City, Country, UserCity
from app.auth.utils import login_manager, mail
from app.error_handlers import page_not_found, internal_server_error

from utils.weather.countries import COUNTRY_API_URL, main as get_countries


def create_app(config_name='default'):
    app = Flask(__name__)
    app.static_folder = 'static'
    app.config.from_object(config[config_name])

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    if config_name == 'testing':
        db = SqliteDatabase(':memory:', pragmas={'foreign_keys': 1})
    else:
        db = SqliteDatabase(app.config['DB_NAME'], pragmas={'foreign_keys': 1})

    database_proxy.initialize(db)
    tables = [Profile, Role, User, Post, Country, City, UserCity]
    db.create_tables(tables)

    if not Country.select().count():
        get_countries(COUNTRY_API_URL)

    csrf = CSRFProtect(app)
    csrf.init_app(app)
    app.config['CSRF'] = csrf

    login_manager.init_app(app)

    Bootstrap(app)

    mail.init_app(app)

    from app.main import main
    from app.auth import auth
    from app.posts import posts
    from app.admin import admin
    from app.weather import weather
    from app.api import api

    csrf.exempt(api)

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(posts)
    app.register_blueprint(admin)
    app.register_blueprint(weather)
    app.register_blueprint(api)

    return app
