import requests


url = "https://api.fungenerators.com/"


def getRando():
    r = requests.get(url + "fact/random")
    r.raise_for_status()
    return r.json()


def getAngel():
    r = requests.get(url + "name/generate?category=angel")
    r.raise_for_status()
    r = r.json()
    return r['contents']['names']
