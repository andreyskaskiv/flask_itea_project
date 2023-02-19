import os
import re
from typing import List


def get_filenames_from_folder(folder: str):
    """Get list of filenames in folder"""
    filenames = os.listdir(folder)
    return filenames


def filter_filenames(filenames: List[str]) -> List[str]:
    """Check filenames format 1900_BoysNames.txt"""
    match_filename = re.compile(r'^[1-2][09][0-9][0-9]_(BoysNames|GirlsNames)\.txt$')
    filtered_filenames = []
    for filename in filenames:
        if match_filename.search(filename):
            filtered_filenames.append(filename)

    return filtered_filenames


def read_data_from_file(read_file: str) -> List[str]:
    """Read data from file"""
    lines = []
    with open(read_file) as file:
        for line in file:
            line = line.strip()
            if line:
                lines.append(line)

    return lines


def filter_data_from_file(lines: List[str]):
    """Filter name and qty names from file"""
    names = []
    match_name = re.compile(r'[a-zA-Z]+')

    for line in lines:
        name = match_name.search(line)

        if name.group():
            name = name.group().capitalize()
            names.append(name)

    return names