from . aws import get_s3_session
import os
from botocore.exceptions import NoCredentialsError


def download_object_from_s3(file_path):
    session = get_s3_session()

    split_file = file_path.split("/")
    length_split = len(split_file) - 1
    file_name = split_file[length_split]
    split_file.pop(length_split)
    s3_folder = "/".join(split_file)

    destination_download = "/tmp/gaussian-splatting/" + file_name

    s3_client = session.s3_client
    s3_client.download_file(session.bucket_name, file_path, destination_download)

    print("destination_download:", destination_download)
    return destination_download, s3_folder


def upload_directory_to_s3(path, destination):
    session = get_s3_session()

    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                file_dest = os.path.join(destination, file)

                try:
                    session.s3_client.upload_file(file_path, session.bucket_name, file_dest)
                except FileNotFoundError:
                    print(f"The file {file_path} was not found - S3 upload failed")
                except NoCredentialsError:
                    print(f"AWS credentials not found - {file} S3 upload failed")
    else:
        print(f"The path {path} is not a directory - S3 upload failed")
