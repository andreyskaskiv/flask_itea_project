import json

from app.weather.configurations.menu import menu


def read_city_id_json(path_to_file):
    with open(path_to_file, 'r', encoding='utf-8') as file:
        city_data = json.load(file)
    return city_data


def create_city_id():
    """city_data:
    {'id': 7669414, 'name': 'Schliern', 'state': '', 'country': 'CH', 'coord': {'lon': 7.41718, 'lat': 46.9105}}
    """

    absolute_path_to_city_names = menu()
    city_data = read_city_id_json(absolute_path_to_city_names)

    valid_cities = [city['name'] for city in city_data]
    # print(valid_cities)
    return valid_cities



