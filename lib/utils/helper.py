from datetime import datetime
import pandas as pd
import MySQLdb
from colorama import init, Fore, Back, Style
from lib.utils.core.settings import *
def log(a):
    """
    Print out variable to screen
        :param a: variable you want to dump
    """
    print(a)

def readCsv(fileName, kolom):
    df = pd.read_csv(fileName, usecols=kolom)
    return df

def banner():
    print("""{}

███████╗██╗███╗   ██╗████████╗ █████╗ ██╗  ██╗    ██████╗  █████╗ ██████╗ ███████╗███████╗██████╗ 
██╔════╝██║████╗  ██║╚══██╔══╝██╔══██╗██║ ██╔╝    ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
███████╗██║██╔██╗ ██║   ██║   ███████║█████╔╝     ██████╔╝███████║██████╔╝███████╗█████╗  ██████╔╝
╚════██║██║██║╚██╗██║   ██║   ██╔══██║██╔═██╗     ██╔═══╝ ██╔══██║██╔══██╗╚════██║██╔══╝  ██╔══██╗
███████║██║██║ ╚████║   ██║   ██║  ██║██║  ██╗    ██║     ██║  ██║██║  ██║███████║███████╗██║  ██║
╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝ [v{}]
{}                                                                                                
[Author]:{}
[Description]:{}
[Download]:{}
[License]:{}
""".format(Fore.BLUE, VERSION,Style.RESET_ALL,AUTHOR,DESCRIPTION,PROJECT_HOMEPAGE,LICENSE))
    
def GenerateNim(angkatan):
    """Generate Nim berdasarkan fakultas."""
    db = MySQLdb.connect(host="localhost",
                         user="root",
                         passwd="",
                         db="stelindb")
    cur = db.cursor()
    dataNim = {}
    fakultas_id = {
        "Sistem Informasi": "N1"
    }

    for fakultas, kode_fakultas in fakultas_id.items():
        cur.execute(
            "SELECT * FROM t_mahasiswa where NIM like '{}.{}.%'"
            .format(angkatan, kode_fakultas))
        NIM_temp_array = []
        for baris in cur.fetchall():
            NIM_temp_array.append(baris[6])
        dataNim[fakultas] = NIM_temp_array
    return dataNim

def saveToFile(data):
    file = open("result.txt", "w")
    for item in data:
        file.write("{} ".format(item))

    tgl = datetime.now().strftime('%Y-%b-%d %H:%M:%S')
    file.write("\nLast checked: {}".format(tgl))
    file.close()