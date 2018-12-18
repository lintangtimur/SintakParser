
try:
    import os
    import requests
    from sintak_parser.Endpoint import Endpoint, Req_Header
    from sintak_parser.utils.core.res_message import ResourceMessage
    from sintak_parser.Parser import SintakParser
    from sintak_parser.utils.helper import log
    from colorama import init, Fore, Back, Style
    from sintak_parser.utils.helper import banner
    from bs4 import BeautifulSoup

    init()
    banner()
except ModuleNotFoundError:
    print("Error")

def checkLogin(func):
    def isLogin(*args, **kwargs):
        """
        Check is already login or not
            :param *args: 
            :param **kwargs: 
        """
        if not args[0].resp == None:
            return func(*args)
        else:
            print("{}[WARNING]Function {}() can be execute if success login first{}".format(
                Fore.YELLOW, func.__name__,Style.RESET_ALL)
            )
            
    return isLogin

class Fetch():
    """
    Fetch Sintak Data
    """

    EXT_IMG = ".jpg"
    PREFIX_FILEKTM = "ktm_"
    
    def __init__(self, username, password):
         
        self.resp = None
        self.session = None
        self.username = username
        
        self.__loginSintakId(username, password)
        

    def __loginSintakId(self, username, password):
        """
        Proses login ke sintak
            :param self: 
            :param username: Nim mahasiswa contoh: 15.N1.0020
            :param password: Password berupa tanggal lahir mahasiswa tersebut
        """   
        LOGINDATA = {
            "user": username,
            "pass": password
        }    

        session = requests.Session()
        self.session = session
        resp = session.post(
            Endpoint.SINTAKID_VALIDATE, data=LOGINDATA, headers=Req_Header.HEADERS
        )
        if resp.text != ResourceMessage.ALERT['wrongCredentials']:
            self.resp = resp.content
            print("{}[INFO] {} success login !{}".format(
                Fore.LIGHTGREEN_EX, username,Style.RESET_ALL)
            )
        else:
            print("{}{}[CRITICAL] {} Failed to login !{}".format(
                Back.RED,Fore.WHITE, username,Style.RESET_ALL)
            )
        
    def IsDashboardAccessible(self):
        """
        Cek apakah bagian dashboard dapat diakses
            :param self: 
        """
        if self.resp == None:
            return False
        return True

    def getResp(self):
        return self.resp

    def getSession(self):
        return self.session

    @checkLogin
    def getESertifikat(self):
        return SintakParser(self.session, Endpoint.SINTAK_URL_ESERTIFIKAT).getSertif()

    @checkLogin
    def getAllIndeksPrestasi(self):
        return self.session.get(Endpoint.SINTAKID_URL_DATA_BAR_CHART, headers=Req_Header.HEADERS).json()
    
    @checkLogin
    def getDataPieChart(self):
        return self.session.get(Endpoint.SINTAKID_URL_DATA_PIE_CHART, headers=Req_Header.HEADERS).json()

    def getTranskrip(self):
        pass

    
    def getKHS(self, smt, tahun):
        """
        Mendapatkan Kartu Hasil Studi berdasarkan semester dan tahun ajar
        
        Args:
            smt (str): semester
            tahun (str): tahun ajar, 2015 sampai 2018
        """
        tahunAjar = ['2015', '2016', '2017', '2018']

        semester = {
            "ganjil" : "G1",
            "genap" : "G2",
            "sisipan" : "S1"
        }

        dataPayload = {
            "smt" : semester[smt],
            "tahun": tahun
        }
        resp = self.session.post(Endpoint.SINTAKID_URL_KHS, data=dataPayload, headers=Req_Header.HEADERS)
        return resp.json()

    def getTagihan(self, tahun, semester):
        """
        Mendapatkan tagihan
        
        Args:
            tahun (str): tahun, contoh 2018,2017
            semester (str): G1,G2
        """

        dataPayload = {
            "th" : tahun,
            "uji": semester
        }
        temp = {
            "kode_mk" : [],
            "nama_mk" : [],
            "sks" : [],
            "kelas": [],
            "status": [],
            "jumlah":[],
            "total": ""
        }

        tableBotTemp = {
            "tagihan" : [],
            "jumlah": [],
            "total" : ""
        }

        resp = self.session.post(Endpoint.SINTAK_URL_TAGIHAN, data=dataPayload, headers=Req_Header.HEADERS).text
        soup = BeautifulSoup(resp, 'html.parser')
        tables = soup.findAll("table", {"cellspacing": 2,"cellpadding":2})
        tableTop = tables[0]
        tableBot = tables[1]

        trData = tableTop.findAll("tr")
        trDataBot = tableBot.findAll("tr")
        
        #======================================= PARSING TABLE BAGIAN ATAS ============================
        for i in range(1, len(trData)-1):
            temp['kode_mk'].append(trData[i].findAll("td")[0].text)
            temp['nama_mk'].append(trData[i].findAll("td")[1].text)
            temp['sks'].append(trData[i].findAll("td")[2].text)
            temp['kelas'].append(trData[i].findAll("td")[3].text)
            temp['status'].append(trData[i].findAll("td")[4].text)
            temp['jumlah'].append(self._parseCurrency(trData[i].findAll("td")[5].text))
        
        total = self._parseCurrency(trData[len(trData)-1].findAll("td")[1].text)
        temp['total'] = total

        #======================================= PARSING TABLE BAGIAN BAWAH ===========================
        for i in range(1, len(trDataBot)-1):
            tableBotTemp['tagihan'].append(trDataBot[i].findAll("td")[0].text)
            tableBotTemp['jumlah'].append(self._parseCurrency(trDataBot[i].findAll("td")[1].text))

        totalBot = self._parseCurrency(trDataBot[len(trDataBot)-1].findAll("td")[1].text)
        tableBotTemp['total'] = totalBot
        return {
            "tableTop" : temp,
            "tableBot" : tableBotTemp
        }

    def _parseCurrency(self, cash):
        return cash.split(',')[0].replace('.',"")

    @checkLogin
    def getKtm(self, saveTo):
        """
        save KTM mahasiswa to directory
            :param self: 
            :param saveTo: directory you want to save in
        """
        if not self.IsDashboardAccessible():
            print("You Must login first!")
        else:
            ktm = SintakParser(self.session, Endpoint.SINTAKID_USER_DASHBOARD).parsingKtm()
            img_data = requests.get(Endpoint.SINTAKID+ktm).content

            currentDirectory = os.getcwd()
            directoryToCreate = saveTo
            if os.path.exists(currentDirectory+directoryToCreate):
                print(ResourceMessage.ALERT['directoryExist'])
            else:
                os.makedirs(directoryToCreate, exist_ok=True)
            
            fileName = self.PREFIX_FILEKTM+self.username+self.EXT_IMG
            completePath = os.path.join(currentDirectory+"\\"+directoryToCreate, fileName)
            
            try:
                with open(completePath, 'wb') as handler:
                    handler.write(img_data)
            except IOError as e:
                print(ResourceMessage.ALERT['errorWriteToFile'])
                print(e)
            finally:
                handler.close()
                print("{}[SAVED] {} saved to {}{}".format(
                    Fore.GREEN, fileName, completePath, Style.RESET_ALL)
                )