import argparse
from pytube import YouTube


def get_video(url):
    url = "".join(url)
    print("[*] Downloading video...\n")
    YouTube(url).streams[0].download()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interact with YouTube.")
    parser.add_argument("-g", "--get", nargs="*", help="Get a video.")
    args = parser.parse_args()
    get_video(args.get)
