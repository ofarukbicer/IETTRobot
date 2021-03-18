# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from requests import get
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class IETT(object):
    def __init__(self, hatdurak):
        self.veri = get(f"http://www.iett.istanbul/tr/main/ajaxHatDurakAra/?q={hatdurak}", verify=False).json()[0]

    @property
    def bilgi_ver(self):
        sozluk = []

        for durak in self.veri['items']:
            if durak['type'] != 'station':
                continue

            sozluk.append({
                'durak_adi'  : durak['name'].replace('İ', 'i').title(),
                'durak_yeri' : durak['location'].replace('İ', 'i').title(),
                'durak_yonu' : durak['yon'].replace('İ', 'i').title(),
                'sefer_bilgi': f"https://iett.istanbul/tr/main/duraklar/{durak['code']}/{durak['name']}-İETT-Duraktan-Geçen-Hatlar-Durak-Bilgileri-Hattın-Duraktan-Geçiş-Saatleri"
            })

        return sozluk

    @property
    def seferler(self):
        return [sefer['sefer_bilgi'] for sefer in self.bilgi_ver]

    @property
    def durak_adlari(self):
        return [sefer['durak_adi'] for sefer in self.bilgi_ver]

    @property
    def durak_yerleri(self):
        return [sefer['durak_yeri'] for sefer in self.bilgi_ver]

    @property
    def durak_yonleri(self):
        return [sefer['durak_yonu'] for sefer in self.bilgi_ver]