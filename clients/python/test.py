import unittest
from lns import Client, IncompatibleServer, NameNotFound

class LNSTest(unittest.TestCase):
    def test_lns_server_connection(self):
        #Test connection to server
        try: Client('https://omicronlns.glitch.me')
        except: self.failureException()

        #test exception raise
        with self.assertRaises(IncompatibleServer):
            Client('google.com')
        
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