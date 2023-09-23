import os, requests
from .common import singleton


class IpApi():
    
    
    _IP_KEY = os.getenv("IP_KEY")

    def __init__(self, ip_address: str) -> None:
        self.ip_address = ip_address
        self.hosting = False
        self.proxy = False
        self.status = 'error'
        


    def get_ip(self):
        url = f"https://pro.ip-api.com/json/{self.ip_address}?fields=status,message,proxy,hosting&key={self._IP_KEY}"

        result = requests.get(url)
        if result.status_code == 200:
            data = result.json()
            self.hosting = data['hosting']
            self.proxy = data['proxy']
            self.status = data['status']
 