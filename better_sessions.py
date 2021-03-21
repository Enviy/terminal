import pathlib
import os

def clear():
    os.system('{0}'.format('clear'))
    return 0

def cwd():
    return pathlib.Path.cwd()


def ls():
    os.system('{0}'.format('ls'))
    return 0
