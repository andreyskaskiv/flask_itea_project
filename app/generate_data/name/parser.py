import os
from pathlib import Path

from app.generate_data.name import baby_names
from app.generate_data.name.handlers.error_handler import check_folder_exist, check_files
from app.generate_data.name.handlers.file_handler import get_filenames_from_folder, filter_filenames
from app.generate_data.name.handlers.name_parser import name_parser


PATH_TO_THE_FOLDER_WITH_NAMES = os.path.join(Path(baby_names.__file__).parent)


def run_parser():
    check_folder_exist(PATH_TO_THE_FOLDER_WITH_NAMES)
    filenames = get_filenames_from_folder(PATH_TO_THE_FOLDER_WITH_NAMES)
    filtered_filenames = filter_filenames(filenames)
    check_filenames = check_files(filtered_filenames)

    if check_filenames:
        return check_filenames

    parsed_names = name_parser(filtered_filenames)

    return parsed_names


# if __name__ == '__main__':
#     print(run_parser()['BoysNames'] + run_parser()['GirlsNames'])

