from xml.etree import ElementTree as ET
from argparse import ArgumentParser
from requests import get
from os import environ
from re import sub


my_key = environ['DICT_KEY']
r_url = 'https://www.dictionaryapi.com/api/v1/references/collegiate/xml/'


def defineWord(word):
    r = get(r_url + word + '?key=' + my_key)
    try:
        root = ET.fromstring(r.content)
    except ET.ParseError:
        return False
    for child in root:
        try:
            if __name__ == "__main__":
                print(child[0].text)
        except IndexError:
            if __name__ == "__main__":
                print("I guess that word isn't here fella.")
            return False
        for subchild in child:
            for dt in subchild.iter('dt'):
                definition = dt.text
                new_def = sub(r'\W+', ' ', str(definition))
                if __name__ == "__main__":
                    print(new_def)
                return True


if __name__ == "__main__":
    parser = ArgumentParser(description='Dictionary definitions.')
    parser.add_argument('word',
                        nargs='*',
                        help='Word to be defined.')
    arg = parser.parse_args()
    word = ' '.join(arg.word)
    defineWord(word)
