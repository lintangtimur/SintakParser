from bs4 import BeautifulSoup
from lib.Endpoint import Endpoint, Req_Header

class SintakParser():
    """
    Module untuk memparsing halaman sintak
    """
    def __init__(self, response):
        self.session = response
        self.content = None
        self.__makeRequest(self.session)

    def parsingKtm(self):   
        """
        Mencari KTM
            :param self: 
        """
        soup = BeautifulSoup(self.content, 'html.parser')
        ktm = soup.findAll('img')[1].get('src')
        return ktm
    
    def __makeRequest(self,session):
        self.content = session.get(Endpoint.SINTAKID_USER_DASHBOARD, headers=Req_Header.HEADERS).content
