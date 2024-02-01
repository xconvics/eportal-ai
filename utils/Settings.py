from requests.cookies import RequestsCookieJar
from utils.CookieLoader import CookieLoader


class Settings:
    COOKIES_FILE_PATH = "cookies.json"
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
        "content-type": "application/json",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        "accept": "application/json, text/javascript, */*; q=0.01"
    }


    @property
    def cookieJar(self) -> RequestsCookieJar:
        cookieLoader = CookieLoader(self.COOKIES_FILE_PATH)
        return cookieLoader.loadAllIntoCookieJar()


settings = Settings()
