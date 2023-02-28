from peewee import CharField, TextField, ForeignKeyField

from app.auth.models import User
from app.base_model import BaseModel
from app.exceptions import ValidationError


class Country(BaseModel):
    code = CharField(max_length=3, unique=True, index=True)
    name = CharField(max_length=150, unique=True, index=True)
    flag = CharField(unique=True)
    description = TextField()

    def to_json(self):
        country = {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'flag': self.flag,
            'description': self.description}
        return country


class City(BaseModel):
    name = CharField(max_length=150, unique=True, index=True)
    country = ForeignKeyField(Country, backref='city')

    def to_json(self):
        city = {
            'id': self.id,
            'name': self.name,
            'country_id': self.country.id,
            'country_name': self.country.name}
        return city

    @staticmethod
    def from_json(city_json):
        name = city_json.get('name')
        if not name:
            raise ValidationError('city does not have a name')

        name = name.capitalize()
        city_exist = City.select().where(City.name == name).first()
        if city_exist:
            raise ValidationError(f'city {city_exist.name} already added in database with id {city_exist.id}')

        return City(name=name)


class UserCity(BaseModel):
    city = ForeignKeyField(City, backref='city_user')
    user = ForeignKeyField(User, backref='city_user')
