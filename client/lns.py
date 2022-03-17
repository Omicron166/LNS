#Written by Omicron166
from json import JSONDecodeError
import requests

#accepted server versions
server_version = 2

#client version
client_version = '2.1.0'

class BadServer(Exception):
    """Raised when the server version doesn't match the client version"""
    pass

class NameNotFound(Exception):
    """Raised when the server don't return the json file"""
    pass

class NetError(Exception):
    """Raised when requests.get throw an exception"""
    pass


class Client(object):
    def __init__(self, server: str):
        """
        Client instance for lns servers.
        \n
        Can throw NetError and BadServer exceptions.
        """
        #url parser
        if server.startswith('lns://'): self.server = server.replace('lns://', 'http://') # lns://host/path like url
        elif server.startswith('lnss://'): self.server = server.replace('lnss://', 'https://') # lnss://host/path like url
        elif server.startswith(('http://', 'https://')): self.server = server # https://host/path like url
        else: self.server = 'http://' + server # host/path like url (schemeless)

        #index.json get request
        try:
            request = requests.get(self.server + '/index.json') #GET /index.json
        except Exception as e:
            raise NetError(e) #Foward net error to dev

        #server checks

        ##status check
        if request.status_code != 200:
            raise BadServer("This isn't a LNS server, request status != 200")
        
        ##json check
        try:
            index = request.json()
        except JSONDecodeError:
            raise BadServer("This isn't a LNS server, json decode error")

        ##version check
        if not index['version'] == server_version:
            raise BadServer("Server version doesn't match client version")
        else: self.index = index


    def resolve(self, name: str):
        """
        Return a string with the value of the resolved name.
        \n
        Can throw NameNotFound exception.
        """
        #Request section
        try:
           r = requests.get(self.server + '/records/' + name + '.json') # GET /records/name.json
        except:
            raise NameNotFound('The record does not exist')
        if r.status_code != 200:
            raise NameNotFound('The record does not exist')

        #Parse section
        try: return r.json()['record']['link']
        except: raise NameNotFound('The record format is invalid')


    def dig(self, name: str):
        """
        Return the parsed json from the server.
        \n
        Can throw NameNotFound exception.
        """
        #Request section
        try:
           r = requests.get(self.server + '/records/' + name + '.json') # GET /records/name.json
        except:
            raise NameNotFound('The record does not exist')
        if r.status_code != 200:
            raise NameNotFound('The record does not exist')

        #Parse section
        try: return r.json()
        except: raise NameNotFound('The record format is invalid')