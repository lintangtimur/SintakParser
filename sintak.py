from time import gmtime, strftime, sleep
import sys
from lib.Fetch import Fetch



try:
    __import__("lib.utils.versioncheck")
except ImportError:
    exit("[!] wrong installation detected (missing modules)")

username = '15.N1.0020'
password = '24/05/199s7'

sintak = Fetch(username, password)
