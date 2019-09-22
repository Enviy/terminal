import wikipedia as wiki
import argparse

parser = argparse.ArgumentParser(description='Search in Wikipedia.')
parser.add_argument('-d', '--dmp', nargs='+', help='a string to search for')
input = parser.parse_args()
search = ' '.join(input.dmp)
#lis = BeautifulSoup(html, "html.parser").find_all('li')

try:
	print(wiki.summary(search, sentences=3))
except wiki.exceptions.DisambiguationError as e:
	print("There are multiple matching results.")
	print(e)
except wiki.exceptions.PageError:
	print("There are no results! Sorry bout it champ.")

