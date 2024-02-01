import requests
import json
import time
from requests import Request
from requests.cookies import RequestsCookieJar
from utils.Settings import settings


# decorator for printing time
def printTime(func):
    def inner(self, url, data=None):
        start_time = time.time()
        res = func(self, url, data)

        f = func.__name__
        method = "GET"
        if f == "post" or f == "post_req":
            method = "POST"

        print(method, url, ":", time.time() - start_time, "s")
        return res

    return inner


# Singleton for RequestSender (keep the same session in all of the requests)
class RequestSenderMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class RequestSender(metaclass=RequestSenderMeta):
    def __init__(
            self,
            headers: dict = settings.HEADERS,
            cookies: RequestsCookieJar = settings.cookieJar
    ) -> None:
        self.session = requests.Session()
        self.session.cookies = cookies
        for header, value in headers.items():
            self.session.headers[header] = value

    @printTime
    def get(self, url: str, data: dict = None):
        res = self.session.get(url, params=data).json()
        return res

    @printTime
    def get_with_headers(self, url: str, data: dict = None):
        res = self.session.get(url, params=data)
        return res.json(), res.headers

    def post(self, url: str, data: dict = None, json: dict = None, headers: dict = None):
        return self.session.post(url, data=data, json=json, headers=headers)

    @printTime
    def post_req(self, url, data):
        req = Request("POST", url, json=data)
        prepped = self.session.prepare_request(req)
        prepped.headers["accept"] = "application/json, text/javascript, */*; q=0.01"
        prepped.headers["accept-language"] = "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"
        prepped.headers["content-type"] = "application/json"
        prepped.headers["accept-encoding"] = "gzip, deflate, br"

        res = self.session.send(prepped)
        return res.json()


requestSender = RequestSender()
