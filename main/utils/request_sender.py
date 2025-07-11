import requests
from fake_useragent import UserAgent

class RequestSender():
    
    def __init__(self, url:str) -> None:
        self.url = url
        
    def send(self) -> int:
        ua = UserAgent()
        headers = {
            "User-Agent": ua.random
        }
        return requests.get(self.url, headers=headers).status_code