import requests


def download_url(url: str, output_file: str):
    r = requests.get(url, verify=False)

    with open(output_file, "wb") as f:
        f.write(r.content)
