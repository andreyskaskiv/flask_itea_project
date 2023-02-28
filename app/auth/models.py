import datetime

import jwt
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from jwt.exceptions import ExpiredSignatureError, DecodeError
from peewee import CharField, DateTimeField, ForeignKeyField, TextField, IntegerField
from werkzeug.security import generate_password_hash, check_password_hash

from app.base_model import BaseModel


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

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.select().where(User.id == user_id).first()

    @property
    def password(self):
        raise AttributeError('password is not a valid attribute')

    @password.setter
    def password(self, password):
        self.__password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.__password_hash, password)

    def is_admin(self):
        if self.role.name == 'admin':
            return True
        return False

    def generate_auth_token(self, expiration=3600):
        """ Creating a token for the user, by default, ending after 3600s """
        token = jwt.encode(
            {
                'id': self.id,
                'exp': datetime.datetime.now().timestamp() + datetime.timedelta(seconds=expiration).seconds
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256')
        return token

    @staticmethod
    def verify_auth_token(token):
        """ Verifying the authenticity of our token """
        try:
            token_data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
        except (ExpiredSignatureError, DecodeError):
            return None
        return User.select().where(User.id == int(token_data['id'])).first()


class Post(BaseModel):
    title = CharField(max_length=100)
    content = TextField(default="")
    date_posted = DateTimeField(default=datetime.datetime.utcnow)
    author = ForeignKeyField(User)
