from peewee import CharField, ForeignKeyField

from app.auth.models import User
from app.base_model import BaseModel


class UserCity(BaseModel):
    city_name = CharField()
    user = ForeignKeyField(User)
