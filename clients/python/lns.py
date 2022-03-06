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
        try: status = requests.get(self.server + '/index.json').json()
        except: raise IncompatibleServer
        if not status['version'] in server_version:
            raise IncompatibleServer()

    def resolve(self, name: str):
        try:
            r = requests.get(self.server + '/records/' + name + '.json')
            if r.status_code != 200: raise NameNotFound()
        except: raise NameNotFound('The record does not exist')

        try: return r.json()['record']['link']
        except: raise NameNotFound('The record format is invalid')

    def dig(self, name: str):
        try:
            if r.status_code != 200: raise Exception()
            r = requests.get(self.server + '/records/' + name + '.json')
        except: raise NameNotFound('The record does not exist')

        try: return r.json()
        except: raise NameNotFound('The record format is invalid')