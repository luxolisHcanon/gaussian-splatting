import zipfile
import shutil


def get_folder_from_path(file_path):
    split_file = file_path.split("/")
    split_file.pop()
    return "/".join(split_file)


def unzip_folder(zip_path):
    print('zip_path =', zip_path)
    folder_path = get_folder_from_path(zip_path)
    print('folder_path =', folder_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(folder_path)
    return folder_path


def clean_files(path):
    shutil.rmtree(path)
