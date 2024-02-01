import requests
import json


class CookieLoader:
    def __init__(
            self,
            file_path: str
    ) -> None:
        self.file_path = file_path

    def loadAllIntoCookieJar(self) -> requests.cookies.RequestsCookieJar:
        jar = requests.cookies.RequestsCookieJar()
        with open(self.file_path) as f:
            cookie_list = json.load(f)
            for cookie in cookie_list:
                jar.set(
                    cookie.get("name"),
                    cookie.get("value"),
                    domain=cookie.get("domain"),
                    path=cookie.get("path")
                )
        return jar
