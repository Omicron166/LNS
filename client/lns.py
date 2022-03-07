#Written by Omicron166

import requests
from urllib.parse import urlparse

#accepted server versions
server_version = 1

#client version
client_version = '1.2.0'

class IncompatibleServer(Exception):
    pass

class NameNotFound(Exception):
    pass

class Client(object):
    def __init__(self, server: str):
        url = urlparse(server)
        if url.scheme == '' or url.scheme == 'lns':
            self.server = 'http://' + url.netloc + url.path #when a schema is not provided, netloc is '' and path has the server url
        else:
            self.server = url.scheme + '://' + url.netloc + url.path
        try: status = requests.get(self.server + '/index.json').json()
        except: raise IncompatibleServer('This is not a LNS server')
        if not index['version'] == server_version:
            raise IncompatibleServer('Version not supported of the server')
        else: self.index = status

    def resolve(self, name: str):
        try:
            r = requests.get(self.server + '/records/' + name + '.json')
        except: raise NameNotFound('The record does not exist')
        if r.status_code != 200: raise NameNotFound('The record does not exist')

        try: return r.json()['record']['link']
        except: raise NameNotFound('The record format is invalid')

    def dig(self, name: str):
        try:
            r = requests.get(self.server + '/records/' + name + '.json')
        except: raise NameNotFound('The record does not exist')
        if r.status_code != 200: raise NameNotFound('The record does not exist')

        try: return r.json()
        except: raise NameNotFound('The record format is invalid')