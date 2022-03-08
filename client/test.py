import unittest
from lns import Client, IncompatibleServer, NameNotFound

server_url = 'omicronlns.glitch.me'

class LNSTest(unittest.TestCase):
    def test_lns_server_http(self):
        #Test connection to server with http scheme
        Client('https://' + server_url)

    def test_lns_server_lns(self):
        #Test connection to server with lns scheme
        Client('lns://' + server_url)

    def test_lns_server_schemeless(self):
        #Test connection to server without scheme
        Client(server_url)

    def test_not_server_detection(self):
        #test exception raise
        with self.assertRaises(IncompatibleServer):
            Client('https://google.com')
        
    def test_lns_resolver(self):
        #test the resolver system
        lns = Client('https://' + server_url)
        self.assertEqual(lns.resolve('template'), 'dns.google.com')

        with self.assertRaises(NameNotFound):
            lns.resolve('paraguay')

    def test_lns_dig(self):
        #test the dig system
        lns = Client('https://' + server_url)
        self.assertEqual(lns.dig('template'), {
            "record_owner": {
                "name": "Omicron166",
                "email": "omicron166@protonmail.com"
            },
            "record": {
                "link": "dns.google.com",
                "txt": "dns like txt record"
            }
        })

        with self.assertRaises(NameNotFound):
            lns.dig('paraguay')

if __name__ == '__main__':
    unittest.main()