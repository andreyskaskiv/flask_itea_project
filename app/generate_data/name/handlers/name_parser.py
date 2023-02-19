import os
import re
from pathlib import Path
from typing import List, NamedTuple, Dict

from app.generate_data.name import baby_names
from app.generate_data.name.handlers.file_handler import read_data_from_file, filter_data_from_file


class Filenames(NamedTuple):
    year: int
    gender: str


def split_file(filtered_filenames: List[str]) -> List[Filenames]:
    """Split 1900_BoysNames.txt -> Filenames(year='1900', gender='BoysNames')"""

    names_file_split = []
    for filenames in filtered_filenames:
        match_split = re.split(r"[_\.]", filenames)
        names_file_split.append(Filenames(int(match_split[0]), match_split[1]))

    return names_file_split


def create_template_data(names_file_split: List[Filenames]):
    """Create a template for the database
    {'BoysNames': [], 'GirlsNames': []}"""

    template_data = {}
    for filename in names_file_split:
        template_data[filename.gender] = []

    return template_data


def get_names(filtered_filename: str):
    path_filtered_filename = os.path.join(Path(baby_names.__file__).parent, filtered_filename)
    lines = read_data_from_file(path_filtered_filename)
    names = filter_data_from_file(lines)
    return names


def parse_data(data_template, filtered_filenames: List[str]):
    """Update database"""

    for _ in data_template:
        for filtered_filename in filtered_filenames:
            if 'BoysNames' in filtered_filename:

                names = get_names(filtered_filename)
                for line in names:
                    data_template['BoysNames'].append(line)
    #
            elif 'GirlsNames' in filtered_filename:

                names = get_names(filtered_filename)
                for line in names:
                    data_template['GirlsNames'].append(line)

            else:
                print('ooops')

    return data_template


def name_parser(filtered_filenames: List[str]):
    """Create a common database"""

    names_file_split = split_file(filtered_filenames)
    data_template = create_template_data(names_file_split)
    parsed_names = parse_data(data_template, filtered_filenames)

    return parsed_names

