#Written by Omicron166
import requests

#accepted server versions
server_version = 2

#client version
client_version = '2.0.0'

class IncompatibleServer(Exception):
    """Raised when the server version doesn't match the client version"""
    pass

class NameNotFound(Exception):
    """Raised when the server don't return status 200"""
    pass

class NetError(Exception):
    """Raised when requests.get throw an exception"""
    pass


class Client(object):
    def __init__(self, server: str):
        #url parser
        if server.startswith('lns://'): self.server = server.replace('lns://', 'http://') # lns://host/path like url
        elif server.startswith('lnss://'): self.server = server.replace('lnss://', 'https://') # lnss://host/path like url
        elif server.startswith(('http://', 'https://')): self.server = server # https://host/path like url
        else: self.server = 'http://' + server # host/path like url (schemeless)


        #server check
        try: index = requests.get(self.server + '/index.json').json()
        except: raise IncompatibleServer('This is not a LNS server')

        #version check
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