from os import environ
from requests import get
from xml.etree import ElementTree as ET
import re
import argparse

parser = argparse.ArgumentParser(description='Retrieve a definition from the Merriam Webster dictionary.')
parser.add_argument('-d', '--dmp', nargs='+', help='the word to be searched for')
input = parser.parse_args()
word = ' '.join(input.dmp)

my_key = environ['DICT_KEY']
#word = input('search for: ')
r_url = 'https://www.dictionaryapi.com/api/v1/references/collegiate/xml/'
request = r_url + word + '?key=' + my_key

def Grab_word():
	r = get(request)
	root = ET.fromstring(r.content)
	for child in root:
		try:
			print(child[0].text)
		except IndexError:
			print("I guess that word isn't here fella.")
			break
		for subchild in child:
			for dt in subchild.iter('dt'):
				definition = dt.text
				new_def = re.sub(r'\W+', ' ', definition)
				print(new_def)

if __name__ == "__main__":
	Grab_word()
