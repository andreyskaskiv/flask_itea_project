import datetime

from flask_login import UserMixin
from peewee import CharField, DateTimeField, ForeignKeyField, TextField, IntegerField
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.base_model import BaseModel


@login_manager.user_loader
def load_user(user_id):
    return User.select().where(User.id == user_id).first()


class Role(BaseModel):
    name = CharField(max_length=100, unique=True, index=True)


class Profile(BaseModel):
    avatar = CharField()
    info = TextField()
    city = CharField()
    age = IntegerField()


class User(BaseModel, UserMixin):
    username = CharField(max_length=100)
    email = CharField(max_length=200, unique=True, index=True)
    __password_hash = CharField(max_length=128)
    last_visit = DateTimeField(default=datetime.datetime.now)

    role = ForeignKeyField(Role, backref='users')
    profile = ForeignKeyField(Profile)


    @property
    def password(self):
        raise AttributeError('password is not a valid attribute')

    @password.setter
    def password(self, password):
        self.__password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.__password_hash, password)

