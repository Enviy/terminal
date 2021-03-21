import argparse
import wikipedia as wiki


def getSearch(search):
    try:
        print(wiki.summary(search, sentences=3))
    except wiki.exceptions.DisambiguationError as e:
        print("[*] There are multiple results:\n", e)
    except wiki.exceptions.PageError:
        print("[!] No results for query. Sorry bout it.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search Wikipedia.')
    parser.add_argument('-s', '--search', nargs='+', help='a topic to search for')
    arg = parser.parse_args()
    if arg.search:
        getSearch(" ".join(arg.search))
