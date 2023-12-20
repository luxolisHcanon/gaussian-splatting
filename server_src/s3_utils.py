from . aws import get_s3_session
import os
from botocore.exceptions import NoCredentialsError
import uuid


def generate_unique_folder(base_path):
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    folder_name = str(uuid.uuid4())
    while os.path.exists(base_path + folder_name):
        folder_name = str(uuid.uuid4())

    os.mkdir(base_path + folder_name)
    return folder_name + "/"


def download_file_from_s3(s3_file_path):
    session = get_s3_session()

    split_file = s3_file_path.split("/")
    length_split = len(split_file) - 1
    file_name = split_file[length_split]
    split_file.pop(length_split)
    s3_folder = "/".join(split_file)

    base_path = "/tmp/gaussian-splatting/"
    downloaded_file_path = base_path + generate_unique_folder(base_path) + file_name

    session.s3_client.download_file(session.bucket_name, s3_file_path, downloaded_file_path)

    print("file_path:", downloaded_file_path)
    return downloaded_file_path, s3_folder


def upload_directory_to_s3(path, destination, session):
    excluded_directory_name = "iteration_7000"

    for root, dirs, files in os.walk(path):
        for directory in dirs:
            if directory != excluded_directory_name:
                upload_directory_to_s3(os.path.join(root, directory), destination, session)
        for file in files:
            file_path = os.path.join(root, file)
            file_dest = os.path.join(destination, file)
            try:
                session.s3_client.upload_file(file_path, session.bucket_name, file_dest)
            except FileNotFoundError:
                print(f"The file {file_path} was not found - S3 upload failed")
            except NoCredentialsError:
                print(f"AWS credentials not found - {file} S3 upload failed")


def upload_full_directory_to_s3(path, destination):
    session = get_s3_session()

    if os.path.isdir(path):
        upload_directory_to_s3(path, destination, session)
    else:
        print(f"The path {path} is not a directory - S3 upload failed")
