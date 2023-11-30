from . aws import get_s3_session
import os
from botocore.exceptions import NoCredentialsError
import uuid
import zipfile


def generate_unique_folder(base_path):
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    folder_name = str(uuid.uuid4())
    while os.path.exists(base_path + folder_name):
        folder_name = str(uuid.uuid4())

    os.mkdir(base_path + folder_name)
    os.mkdir(base_path + folder_name + "/zip_file")
    return folder_name


def unzip_file(file_path, destination_path):
    # Unzip
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(destination_path)

    # Get file name
    files = os.listdir(destination_path)
    if len(files) == 1:
        return files[0]
    else:
        raise Exception("Zip file does not contain exactly one file.")


def download_and_unzip_file_from_s3(file_path):
    session = get_s3_session()

    split_file = file_path.split("/")
    length_split = len(split_file) - 1
    file_name = split_file[length_split]
    split_file.pop(length_split)
    s3_folder = "/".join(split_file)

    base_path = "/tmp/gaussian-splatting/"
    workdir = base_path + generate_unique_folder(base_path)
    file_zip_path = workdir + "/zip_file/" + file_name

    s3_client = session.s3_client
    s3_client.download_file(session.bucket_name, file_path, file_zip_path)

    extracted_file_path = unzip_file(file_zip_path, workdir)
    print("file_path:", extracted_file_path)
    return extracted_file_path, s3_folder


def upload_directory_to_s3(path, destination, session):
    for root, dirs, files in os.walk(path):
        for directory in dirs:
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
