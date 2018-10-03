import sys
import importlib

PYVERSION = sys.version.split()[0]


if PYVERSION >= "3":

    pkg = ['colorama','requests','bs4','var_dump','MySQLdb','pandas']
    for p in pkg:
        spam_spec = importlib.util.find_spec(p)
        if spam_spec == None:
            print("Packages {} is missing, please install it first".format(p))
else:
    print("Will work in Python 3 version")