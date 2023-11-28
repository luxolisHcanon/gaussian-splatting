import requests


def upload_in_s3(url_upload, dir_to_upload):
    upload_result = requests.put(
        url_upload,
        data=open(dir_to_upload, 'rb'),
        headers={
            'Content-Type': 'application/octet-stream',
        });
