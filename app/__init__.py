from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mail import Mail
from peewee import SqliteDatabase

from app.base_model import database_proxy
from app.config import config
from app.error_handlers import page_not_found, internal_server_error

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
mail = Mail()


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
    app.config['db'] = db

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

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(posts)
    app.register_blueprint(admin)
    app.register_blueprint(weather)

    return app
