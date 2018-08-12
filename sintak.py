from time import gmtime, strftime, sleep
import sys
from lib.Fetch import Fetch



try:
    __import__("lib.utils.versioncheck")
except ImportError:
    exit("[!] wrong installation detected (missing modules)")

# # a = readCsv('MhsAktif_SistemInformasi.csv', ['NIM','TGL LAHIR'])
# # username = a['NIM'][0]
# # password = a['TGL LAHIR'][0]

username = '15.N1.0020'
password = '24/05/199s7'

sintak = Fetch(username, password)