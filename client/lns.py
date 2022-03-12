#Written by Omicron166

import requests
from urllib.parse import urlparse

#accepted server versions
server_version = 2

#client version
client_version = '2.0.0'

class IncompatibleServer(Exception):
    pass

class NameNotFound(Exception):
    pass

class Client(object):
    def __init__(self, server: str):
        #url parser
        if server.startswith('lns://'): self.server = server.replace('lns://', 'http://')
        elif server.startswith(('http://', 'https://')): self.server = server
        else: self.server = 'http://' + server

        try: index = requests.get(self.server + '/index.json').json()
        except: raise IncompatibleServer('This is not a LNS server')
        if not index['version'] == server_version:
            raise IncompatibleServer('Version not supported of the server')
        else: self.index = index

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