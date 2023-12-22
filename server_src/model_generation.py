import glob
import os
import shutil
import subprocess

from . s3_utils import download_file_from_s3, upload_full_directory_to_s3
from . file_utils import create_input_folder, unzip_folder, clean_files


def split_video_into_pictures(video_path, destination_path):
    # Split Video into pictures
    subprocess.run(["ffmpeg", "-i", video_path, "-qscale:v", "1", "-qmin", "1", "-vf", "fps=2", "%04d.jpg"])

    # Create input folder and move all photos in it
    for photo in glob.glob('./*.jpg'):
        shutil.move(photo, destination_path)


def generate_nerf_model_from_photo_set(workdir_path):
    # Process the photos
    subprocess.run(["python", "./gaussian_splatting_src/convert.py", "-s", workdir_path, "--no_gpu"])


def generate_model_from_nerf_model(workdir_path):
    # Train the model
    subprocess.run(["python", "./gaussian_splatting_src/train.py", "-s", workdir_path])

    # Move output folder to work directory
    shutil.move("./output", workdir_path)
    output_folder_path = os.path.join(workdir_path, "output")
    return output_folder_path


def generate_and_upload_3d_model(workdir_path, s3_folder):
    generate_nerf_model_from_photo_set(workdir_path)
    model_output_folder = generate_model_from_nerf_model(workdir_path)
    upload_full_directory_to_s3(model_output_folder, s3_folder)
    # clean_files(nerf_model_path)


async def generate_and_upload_3d_model_from_video(s3_path):
    try:
        video_path, s3_folder = download_file_from_s3(s3_path)
        workdir_path, input_folder_path = create_input_folder(video_path)
        split_video_into_pictures(video_path, input_folder_path)
        generate_and_upload_3d_model(workdir_path, s3_folder)
    except Exception as e:
        print(f"Exception raised: {e}")
        return 500
    return 200


async def generate_and_upload_3d_model_from_photos(s3_path):
    try:
        zip_path, s3_folder = download_file_from_s3(s3_path)
        workdir_path, input_folder_path = create_input_folder(zip_path)
        unzip_folder(zip_path, input_folder_path)
        generate_and_upload_3d_model(workdir_path, s3_folder)
    except Exception as e:
        print(f"Exception raised: {e}")
        return 500
    return 200
