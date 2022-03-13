from http.server import HTTPServer, BaseHTTPRequestHandler
import os
from configparser import ConfigParser
import socketserver
from sys import exit #Pyinstaller binaries don't have exit function by default

class StaticServer(BaseHTTPRequestHandler):
    def __init__(self, request: bytes, client_address: tuple[str, int], server: socketserver.BaseServer) -> None:
        super().__init__(request, client_address, server)
        self.root = getconf()['ROOTDIR']

    def do_GET(self):
        root = self.root

        #avoid access to external files
        if '..' in self.path:
            self.send_response_only(400)
            pass
        
        #file check
        filename = root + self.path
        if not os.path.isfile(filename):
            self.send_response_only(400)
            pass
        
        #headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        #send file
        with open(filename, 'rb') as fh:
            html = fh.read()
            self.wfile.write(html)
            fh.close()

def run(addr, port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, StaticServer)
    print('Starting httpd on port {}'.format(port))
    httpd.serve_forever()

def getconf():
    config = ConfigParser()
    if not os.path.isfile('server.conf'):
        #Create default config for testing
        config['SERVER'] = {'HOST': '', 'PORT': 8000, 'ROOTDIR': '.'}

        #Write to server.conf
        with open('server.conf', 'w') as file:
            config.write(file)
            file.close()

    else: config.read('server.conf')
    return config

if __name__ == '__main__':
    conf = getconf()
    try:
        run(
            conf['SERVER']['HOST'],
            int(conf['SERVER']['PORT'])
        )
    except KeyboardInterrupt:
        print('Exiting...')
        exit()