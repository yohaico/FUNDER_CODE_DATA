"""
    Utility for getting all extension files in directory.
"""
import re
import pathlib
import os
import zipfile


def make_dirs_if_needed(path_of_dir):
    # os.makedirs(path, exist_ok=True)
    path = pathlib.Path(path_of_dir)
    path.mkdir(parents=True, exist_ok=True)


def sorted_by_alpha_numeric(data):
    convert_lambda = lambda text: int(text) if text.isdigit() else text.lower()
    alpha_num_key_lambda = lambda key: [convert_lambda(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alpha_num_key_lambda)


def get_files_path_by_ext_top_dir(files_dir: str, ext: str) -> list:
    """
        Scan the directory and return a list of files that match in the top directory only.
    :param str files_dir: the top directory to scan
    :param str ext: the extension to look for
    :return list{str}: the list of matching files
    """

    file_list = list()
    # top directory only * recursive **
    file_list = list(x.as_posix() for x in pathlib.Path(files_dir).glob('*.' + ext))
    # sorting the list by lexicographical order across all OSs
    file_list = sorted_by_alpha_numeric(file_list)
    return file_list


def get_files_path_by_ext_all_dir(files_dir: str, ext: str) -> list:
    """
        Scan the directory and return a list of files that match in the top directory only.
    :param str files_dir: the top directory to scan
    :param str ext: the extension to look for
    :return list{str}: the list of matching files
    """

    file_list = list()
    # top directory only * recursive **
    file_list = list(x.as_posix() for x in pathlib.Path(files_dir).glob('**/*.' + ext))
    # sorting the list by lexicographical order across all OSs
    file_list = sorted_by_alpha_numeric(file_list)
    return file_list


def get_sub_dir(path):
    return os.listdir(path)


def get_all_file_paths(directory):
    # initializing empty file paths list
    file_paths = []

    # crawling through directory and subdirectories
    for root, directories, files in os.walk(directory):
        for filename in files:
            # join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    # returning all file paths
    return file_paths


def unzip_file(path_to_zip_file, directory_to_extract_to):
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory_to_extract_to)


def zip_files(path_to_zip_file, directory_to_zip):
    file_paths = get_all_file_paths(directory_to_zip)
    with zipfile.ZipFile(path_to_zip_file, 'w') as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file, arcname=pathlib.Path(file).name)
