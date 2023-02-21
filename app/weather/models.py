from peewee import CharField, TextField, ForeignKeyField

from app.base_model import BaseModel
from app.auth.models import User


class Country(BaseModel):
    code = CharField(max_length=3, unique=True, index=True)
    name = CharField(max_length=150, unique=True, index=True)
    flag = CharField(unique=True)
    description = TextField()


class City(BaseModel):
    name = CharField(max_length=150, unique=True, index=True)
    country = ForeignKeyField(Country, backref='city')


class UserCity(BaseModel):
    city = ForeignKeyField(City, backref='city_user')
    user = ForeignKeyField(User, backref='city_user')
