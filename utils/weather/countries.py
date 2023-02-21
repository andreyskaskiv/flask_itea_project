import requests
from typing import NamedTuple

from app.weather.models import Country

COUNTRY_API_URL = 'https://restcountries.com/v3.1/all'


class CountryDTO(NamedTuple):
    code: str
    name: str
    flag: str
    description: str


def get_countries(url: str):
    response = requests.get(url)

    response_code = response.status_code
    countries_data = response.json()

    if response_code != 200:
        raise RuntimeError(f'Error: {countries_data["message"]} Status code: {response_code}')
    return countries_data


def parse_countries(countries_raw: list[dict]):
    countries_parsed = []
    for country in countries_raw:
        country_dto = CountryDTO(
            code=country['cca2'],
            name=country['name']['official'],
            flag=country['flags']['png'],
            description=country['flags'].get('alt', 'no data'))
        countries_parsed.append(country_dto)
    return countries_parsed


def write_countries_to_db(countries: list[CountryDTO]):
    for country in countries:
        country_entity = Country(code=country.code,
                                 name=country.name,
                                 flag=country.flag,
                                 description=country.description)
        country_entity.save()


def main(url: str):
    countries_raw = get_countries(url)
    countries_parsed = parse_countries(countries_raw)
    write_countries_to_db(countries_parsed)

