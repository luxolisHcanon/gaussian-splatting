import zipfile
import shutil
import os


def get_folder_from_path(file_path):
    split_file = file_path.split("/")
    split_file.pop()
    return "/".join(split_file)


def unzip_folder(zip_path, destination_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(destination_path)


def create_input_folder(file_path):
    workdir_path = get_folder_from_path(file_path)
    input_folder_path = os.path.join(workdir_path, "input")
    if not os.path.exists(input_folder_path):
        os.makedirs(input_folder_path)
    return workdir_path, input_folder_path


def clean_files(path):
    shutil.rmtree(path)
