
try:
    import os
    import requests
    from lib.Endpoint import Endpoint, Req_Header
    from lib.Parser import SintakParser
    from lib.utils.helper import log
    from colorama import init, Fore, Back, Style
    from lib.utils.helper import banner
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
            print("{}[WARNING]Function {}() can be execute if success login first{}".format(Fore.YELLOW, func.__name__,Style.RESET_ALL))
            
    return isLogin

class Fetch():
    """
    Fetch Sintak Data
    """

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
        resp = session.post(Endpoint.SINTAKID_VALIDATE, data=LOGINDATA, headers=Req_Header.HEADERS)
        if resp.text != 'Username atau Password yang anda masukkan salah.':
            self.resp = resp.content
            print("{}[INFO] {} success login !{}".format(Fore.LIGHTGREEN_EX, username,Style.RESET_ALL))
        else:
            print("{}{}[CRITICAL] {} Failed to login !{}".format(Back.RED,Fore.WHITE, username,Style.RESET_ALL))
        
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
                print("Exist")
            else:
                os.makedirs(directoryToCreate, exist_ok=True)
            
            fileName = 'ktm_'+self.username+'.jpg'
            completePath = os.path.join(currentDirectory+"\\"+directoryToCreate, fileName)
            
            try:
                    with open(completePath, 'wb') as handler:
                        handler.write(img_data)
                # finally:
                #     handler.close()
            except IOError as e:
                print("error write to file")
                print(e)
            finally:
                handler.close()
                print("{}[SAVED] {} saved to {}{}".format(Fore.GREEN, fileName, completePath, Style.RESET_ALL))