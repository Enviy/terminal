import argparse
import pathlib
import hashlib
import requests
from tqdm import tqdm


def grabFile(url):
    url = "".join(url)
    r = requests.head(url)
    total_size = int(r.headers.get('content-length', 0))

    fileName = url.split("/")[-1]
    filePath = str(pathlib.Path.home()) + "/Downloads/{0}".format(fileName)

    # resume_bytes = "bytes={0}-".format(pathlib.Path(filePath).stat().st_size)
    # resume_header = {"Range": resume_bytes}

    with requests.get(url, stream=True, allow_redirects=True) as r:
        r.raise_for_status()
        if r.headers.get('Content-Length') == None:
            print("[!] Content-Length not set. Cannot correctly download.")
            return None
        initial_pos = 0

        with open(filePath, "wb+") as f:
            with tqdm(total=total_size,
                    unit="B",
                    unit_scale=True,
                    desc=fileName,
                    initial=initial_pos,
                    ascii=True) as pbar:
                for chunk in r.iter_content(chunk_size=None):
                    f.write(chunk)
                    pbar.update(len(chunk))
    getHash(filePath)


def getHash(filePath):
    with open(filePath, 'rb') as f:
        content = f.read()
    sha = hashlib.sha256()
    sha.update(content)
    print(sha.hexdigest())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a file at a URL.")
    parser.add_argument("-g", "--get", nargs="*", help="Download a file.")
    args = parser.parse_args()
    grabFile(args.get)
