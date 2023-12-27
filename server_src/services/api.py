import requests


def post_request(url, payload, x_access_token=None):
    headers = {}
    if x_access_token is not None:
        headers = {"x-access-token": x_access_token}
    result = requests.post(url, headers=headers, data=payload)
    return result
