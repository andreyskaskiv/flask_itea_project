import os
from pathlib import Path
from typing import List

from app.generate_data.name import baby_names


def check_folder_exist(folder: str):
    """Check folder exist"""
    if not os.path.exists(folder):
        print(os.path.exists(folder))
        raise FileExistsError(f'Folder {folder} not exist')


def check_files(filtered_filenames: List[str]):
    """Check exist file and txt format"""
    for filtered_filename in filtered_filenames:
        path_filtered_filename = os.path.join(Path(baby_names.__file__).parent, filtered_filename)

        try:
            with open(path_filtered_filename, mode='rt') as file:
                file.read()
        except FileNotFoundError as error:
            return error
        except UnicodeDecodeError:
            return 'Application works only with txt files.'
