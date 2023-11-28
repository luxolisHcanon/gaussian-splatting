import requests

def download_in_s3(url_download, file_to_download):
    print("Downloading USDZ File")
    # download file
    sess = Path(tempfile.mkdtemp())
    filename = 'upload.usdz'
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
