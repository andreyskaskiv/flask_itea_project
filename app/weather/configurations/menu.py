from app import weather
from app.weather.configurations.reading_config import (get_config,
                                                       get_config_settings)

DEFAULTS = "defaults.cfg"
BASE_FOLDER = weather


def menu():
    config, base_dir = get_config(BASE_FOLDER, DEFAULTS)
    absolute_path_to_city_names = get_config_settings(config, base_dir)

    return absolute_path_to_city_names


