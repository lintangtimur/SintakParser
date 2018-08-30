from bs4 import BeautifulSoup
from lib.Endpoint import Endpoint, Req_Header

class SintakParser():
    """
    Module untuk memparsing halaman sintak
    """
    def __init__(self, response, url):
        self.session = response
        self.content = None
        self.__makeRequest(self.session, url)

    def parsingKtm(self):
        """
        Mencari KTM
            :param self: 
        """
        soup = BeautifulSoup(self.content, 'html.parser')
        ktm = soup.findAll('img')[1].get('src')
        return ktm
    
    def __makeRequest(self,session, url):
        self.content = session.get(url, headers=Req_Header.HEADERS).content

    def getSertif(self):
        """
        parsing sertifikat
            :param self: 
        """
        soup = BeautifulSoup(self.content, 'html.parser')
        temp = [
            {'TEMA': []},
            {'JENIS': []},
            {'TGL_MULAI': []},
            {'TGL_AKHIR': []},
            {'PERAN': []},
        ]
        for tbody in soup.findAll('tbody'):
            for tr in tbody.findAll('tr'):
                a = tr.findAll('td')
                if a[0].text == 'Tidak ada Data':
                    return None
                else:
                    temp[0]['TEMA'].append(a[0].text)
                    temp[1]['JENIS'].append(a[1].text)
                    temp[2]['TGL_MULAI'].append(a[2].text)
                    temp[3]['TGL_AKHIR'].append(a[3].text)
                    temp[4]['PERAN'].append(a[4].text)
        return temp