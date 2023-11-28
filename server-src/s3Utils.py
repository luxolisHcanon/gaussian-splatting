import requests
import tempfile
from pathlib import Path


def download_in_s3(url_download):
    print("Downloading Video")
    # download file
    temp_directory = Path(tempfile.mkdtemp())
    filename = 'video.mov'
    video = temp_directory / filename
    video.write_bytes(requests.get(url_download).content)


def upload_in_s3(url_upload, dir_to_upload):
    print("uploading output folder")
    upload_result = requests.put(
        url_upload,
        data=open(dir_to_upload, 'rb'),
        headers={
            'Content-Type': 'application/octet-stream',
        });
