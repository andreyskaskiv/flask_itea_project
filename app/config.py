import os
from pathlib import Path


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(32))
    DB_NAME = os.getenv('DATABASE', 'test.db')
    BASE_DIR = Path(__file__).parent.parent

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
