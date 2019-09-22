import requests

def Catfacts():
	r = requests.get('https://catfact.ninja/fact')
	raw = r.json()
	print(raw['fact'])
Catfacts()
