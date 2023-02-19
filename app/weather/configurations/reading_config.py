import configparser
import os
from pathlib import Path


def get_config(base_folder, file_name: str):
    """
    Get config path.
    @param str file_name: read write file name
    @param base_folder: folder where the file is located

    @return str: absolute path to the file and config
    """
    base_dir = Path(base_folder.__file__).parent
    path_to_config = os.path.join(base_dir, file_name)

    config = configparser.ConfigParser()
    config.read(path_to_config)
    return config, base_dir


def get_config_settings(config, base_dir):
    """Read in `defaults.cfg` to obtain default configuration values."""
    directory_of_cities = config["SETTINGS"]["DIRECTORY_OF_CITIES"]
    file_name_with_city_names = config["SETTINGS"]["FILE_NAME_WITH_CITY_NAMES"]

    absolute_path_to_the_directory = os.path.join(base_dir, directory_of_cities)
    absolute_path_to_city_names = os.path.join(absolute_path_to_the_directory, file_name_with_city_names)

    return absolute_path_to_city_names
