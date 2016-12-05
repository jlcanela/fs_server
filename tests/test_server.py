import sys
sys.path.append('../')

import unittest
import urllib2
import urllib
import time
import json
from multiprocessing import Process

from server.app import app

PORT = 8080


class ServerHandlerTest(unittest.TestCase):
    server = Process(target=app.run)

    @classmethod
    def setUpClass(cls):
        cls.server.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
        cls.server.join()

    def assertContent(self, content, response):
        for line in response.readlines():
            if line == content:
                found = True
        self.assertTrue(found)

    def test_should_give_price_quote_on_received_order(self):
        req = urllib2.Request('http://localhost:%s/quote' % PORT)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps({'nb_days': 1, 'nb_travelers': 3}))
        self.assertEqual(json.loads(response.read()), {'quote' : 5.4})


if __name__ == '__main__':
    unittest.main()
