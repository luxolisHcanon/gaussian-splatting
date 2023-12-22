import glob
import os
import shutil
import subprocess

from . s3_utils import download_file_from_s3, upload_full_directory_to_s3
from . file_utils import get_folder_from_path, unzip_folder, clean_files


def split_video_into_pictures(video_path):
    # Split Video into pictures
    subprocess.run(["ffmpeg", "-i", video_path, "-qscale:v", "1", "-qmin", "1", "-vf", "fps=2", "%04d.jpg"])

    return get_folder_from_path(video_path)


def generate_nerf_model_from_photo_set(photos_path):
    # Create input folder and move all photos in it
    input_folder_path = os.path.join(photos_path, "input")
    if not os.path.exists(input_folder_path):
        os.makedirs(input_folder_path)
    for photo in glob.glob('./*.jpg'):
        shutil.move(photo, input_folder_path)

    # Process the photos
    subprocess.run(["python", "./gaussian_splatting_src/convert.py", "-s", photos_path, "--no_gpu"])

    return photos_path


def generate_model_from_nerf_model(nerf_model_path):
    # Train the model
    subprocess.run(["python", "./gaussian_splatting_src/train.py", "-s", nerf_model_path])

    # Move output folder to work directory
    shutil.move("./output", nerf_model_path)
    output_folder_path = os.path.join(nerf_model_path, "output")
    return output_folder_path


def generate_and_upload_3d_model(photos_path, s3_folder):
    nerf_model_path = generate_nerf_model_from_photo_set(photos_path)
    model_output_folder = generate_model_from_nerf_model(nerf_model_path)
    upload_full_directory_to_s3(model_output_folder, s3_folder)
    # clean_files(nerf_model_path)


async def generate_and_upload_3d_model_from_video(s3_path):
    try:
        video_path, s3_folder = download_file_from_s3(s3_path)
        photos_path = split_video_into_pictures(video_path)
        generate_and_upload_3d_model(photos_path, s3_folder)
    except Exception as e:
        print(f"Exception raised: {e}")
        return 500
    return 200


async def generate_and_upload_3d_model_from_photos(s3_path):
    try:
        zip_path, s3_folder = download_file_from_s3(s3_path)
        photos_path = unzip_folder(zip_path)
        generate_and_upload_3d_model(photos_path, s3_folder)
    except Exception as e:
        print(f"Exception raised: {e}")
        return 500
    return 200
