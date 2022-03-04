#Before running this script, run python -m http.server in the server folder

from lns import Client #The actual client
from lns import IncompatibleServer, NameNotFound #Errors raised by the client

try:
    resolver = Client('http://localhost:8000')
except IncompatibleServer:
    #The server is not compatible with yout client
    pass

print(resolver.resolve('template'))
#Expected output: dns.google.com

try:
    print(resolver.resolve('Paraguay'))
except NameNotFound: #When a name can't be resolved, the client raise this exception
    print('The regsitry does not exists')
