from . s3_utils import download_object_from_s3, upload_directory_to_s3


def split_video_into_pictures(video_path):
    return "photoPath"


def generate_nerf_model_from_photo_set(photos_path):
    return "nerfModelPath"


def generate_model_from_nerf_model(nerf_model_path):
    return "model_output_folder"


async def generate_and_upload_3d_model(s3_path):
    video_path, s3_folder = download_object_from_s3(s3_path)
    photos_path = split_video_into_pictures(video_path)
    nerf_model_path = generate_nerf_model_from_photo_set(photos_path)
    model_output_folder = generate_model_from_nerf_model(nerf_model_path)
    upload_directory_to_s3(model_output_folder, s3_folder)
