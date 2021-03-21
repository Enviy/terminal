import argparse
import os
import requests
from wordnik_client import Client


def getRandDefinition(word):
    word = " ".join(word)
    c = Client()
    definitions = c.GetWord(word, "definitions")
    for i in definitions:
        print(i)

def getDefinition(word):
    word = " ".join(word)
    key = os.environ.get("MERRIAM_DICT")
    if not key:
        print("[!] Failed to find merriam webster key")
        return None
    url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/{0}?key={1}"
    r = requests.get(url.format(word, key))
    r.raise_for_status()
    resp = r.json()
    for i in resp:
        if not isinstance(i, dict):
            return None
        if i.get('shortdef'):
            for definition in i['shortdef']:
                print(definition)
    #return resp


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interact with wordnik_client.")
    parser.add_argument("-r", "--random", nargs="*", help="Word appears in random definitions.")
    parser.add_argument("-d", "--define", nargs="*", help="Define a word.")
    args = parser.parse_args()
    if args.define:
        getDefinition(args.define)
    if args.random:
        getRandDefinition(args.random)
