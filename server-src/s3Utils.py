import requests
import tempfile
from pathlib import Path


def download_in_s3(url_download):
    print("Downloading USDZ File")
    # download file
    sess = Path(tempfile.mkdtemp())
    filename = 'video.mov'
    file_usdz = sess / filename
    file_usdz.write_bytes(requests.get(url_download).content)

    filename = 'upload.glb'
    file_glb = sess / filename


def upload_in_s3(url_upload, dir_to_upload):
    print("uploading output folder")
    upload_result = requests.put(
        url_upload,
        data=open(dir_to_upload, 'rb'),
        headers={
            'Content-Type': 'application/octet-stream',
        });
