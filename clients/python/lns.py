import requests
from urllib.parse import urlparse

#accepted server version
server_version = [1]

class IncompatibleServer(Exception):
    pass

class NameNotFound(Exception):
    pass


class Client(object):
    def __init__(self, server: str):
        url = urlparse(server)
        if not url.scheme:
            self.server = 'http://' + url.netloc
        else:
            self.server = url.scheme + '://' + url.netloc
        status = requests.get(self.server + '/version.json').json()
        if not status['version'] in server_version:
            raise IncompatibleServer()

    def resolve(self, name: str):
        try:
            r = requests.get(self.server + '/' + name)
            if r.status_code != 200: raise Exception()
        except: raise NameNotFound('The record does not exist')

        try: return r.json()['record']['link']
        except: raise NameNotFound('The record format is invalid')

    def dig(self, name: str):
        try:
            r = requests.get(self.server + '/' + name)
            if r.status_code != 200: raise Exception()
        except: raise NameNotFound('The record does not exist')

        try: return r.json()
        except: raise NameNotFound('The record format is invalid')