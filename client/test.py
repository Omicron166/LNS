import unittest
from lns import Client, IncompatibleServer, NameNotFound

class LNSTest(unittest.TestCase):
    def test_lns_server_http(self):
        #Test connection to server with http scheme
        Client('https://omicronlns.glitch.me')

    def test_lns_server_lns(self):
        #Test connection to server with lns scheme
        Client('lns://omicronlns.glitch.me')

    def test_lns_server_schemeless(self):
        #Test connection to server without scheme
        Client('omicronlns.glitch.me')

        #test exception raise
        with self.assertRaises(IncompatibleServer):
            Client('https://google.com')
        
    def test_lns_resolver(self):
        #test the resolver system
        lns = Client('https://omicronlns.glitch.me')
        self.assertEqual(lns.resolve('template'), 'dns.google.com')

    def test_lns_dig(self):
        #test the dig system
        lns = Client('https://omicronlns.glitch.me')
        self.assertEqual(lns.dig('template'), {
            "recorder": "Omicron166",
            "record": {
                "link": "dns.google.com",
                "txt": "dns like txt record"
            }
        })

if __name__ == '__main__':
    unittest.main()