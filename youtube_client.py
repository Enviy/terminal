import argparse
from pytube import YouTube
from pytube.cli import on_progress

# get_video collect highest resolution of url.
def get_video(url):
    url = "".join(url)
    print("[*] Downloading video...\n")
    yt = YouTube(url, on_progress_callback=on_progress)
    strem = yt.streams.get_highest_resolution()
    if strem is not None:
        strem.download()
    else:
        print("[!] No highest resolution found; None type returned.")
  
  
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interact with YouTube.")
    parser.add_argument("-g", "--get", nargs="*", help="Get a video.")
    args = parser.parse_args()
    get_video(args.get)
