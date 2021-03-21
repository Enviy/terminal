from pathlib import Path
import os


def dir_walk(d, e):
	# d = directory to iterate
	# e = extension of file to handle
	if Path(d).exists():
		directory = d
	else:
		print('[!] {0} is not a directory'.format(d))
	for fn in os.listdir(directory):
		if fn.endswith(e):
			with open(fn) as f:
				lines = f.read()
			## do a thing ##
			return lines
