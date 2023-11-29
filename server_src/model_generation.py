import glob
import os
import shutil
import subprocess

from .s3_utils import download_object_from_s3, upload_directory_to_s3


def split_video_into_pictures(video_path):
    print("video_path =", video_path)

    # Split Video into pictures
    subprocess.run(["ffmpeg", "-i", video_path, "-qscale:v", "1", "-qmin", "1", "-vf", "fps=5", "%04d.jpg"])

    # Remove the file from the path to get the work directory
    split_video_path = video_path.split("/")
    split_video_path.pop()
    photo_path = "/".join(split_video_path)
    return photo_path


def generate_nerf_model_from_photo_set(photos_path):
    print("photos_path =", photos_path)

    # Create input folder and move all photos in it
    input_folder_path = os.path.join(photos_path, "input")
    os.mkdir(input_folder_path)
    for photo in glob.glob(f'{photos_path}/*.jpg'):
        shutil.move(photo, input_folder_path)

    return "nerfModelPath"


def generate_model_from_nerf_model(nerf_model_path):
    print("nerf_model_path =", nerf_model_path)
    return "model_output_folder"


async def generate_and_upload_3d_model(s3_path):
    video_path, s3_folder = download_object_from_s3(s3_path)
    photos_path = split_video_into_pictures(video_path)
    nerf_model_path = generate_nerf_model_from_photo_set(photos_path)
    model_output_folder = generate_model_from_nerf_model(nerf_model_path)
    upload_directory_to_s3(model_output_folder, s3_folder)
