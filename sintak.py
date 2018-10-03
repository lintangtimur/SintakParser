from time import gmtime, strftime, sleep
import sys
from lib.Fetch import Fetch


try:
    __import__("lib.utils.versioncheck")
    
except ImportError:
    exit("[!] wrong installation detected (missing modules)")


# username = '17.G4.0009'
# password = '10/2/2000'
def sertifF(var):
    print("E-Sertifikat")
    for index in range(len(var[0]['TEMA'])):
        tema = var[0]['TEMA'][index]
        jenis = var[1]['JENIS'][index]
        tgl_mulai = var[2]['TGL_MULAI'][index]
        tgl_akhir = var[3]['TGL_AKHIR'][index]
        peran = var[4]['PERAN'][index]
        
        print("Tema: {}, Jenis: {}, Tgl Mulai: {}, Tgl Akhir: {}, Peran: {}".format(tema, jenis, tgl_mulai, tgl_akhir, peran))

def ips(var):
    for index in range(len(var[0]['data'])):
        periode = var[0]['data'][index]
        ip = var[1]['data'][index]
        print("Periode: {}, IP: {}".format(periode, ip))

def run(ip,ser):
    if ser is not None:
        sertifF(ser)
    else:
        pass
    
    if ip is not None:
        ips(ip)
    else:
        pass
    

username = '15.N1.0020'
password = '01/05/1997'
sintak = Fetch(username, password)

sertif = sintak.getESertifikat()
ip = sintak.getAllIndeksPrestasi()
sintak.getKtm('ktm')

run(ip, sertif)
