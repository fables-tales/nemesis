import httplib
import unittest
import random
import urllib
import sys
import os
sys.path.insert(0,os.path.abspath('../nemesis/'))
import helpers

def delete_db():
    conn = helpers.sqlite_connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM registrations")
    conn.commit()

def get_registrations():
    conn = helpers.sqlite_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM registrations")
    return list(cur)

def server_post(endpoint, params=None):
    conn = httplib.HTTPConnection("localhost:5000")
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}
    if params != None:
        url_params = urllib.urlencode(params)
        conn.request("POST", endpoint, url_params, headers)
    else:
        conn.request("POST", endpoint)

    return conn.getresponse()


def server_get(endpoint, params=None):
    conn = httplib.HTTPConnection("localhost:5000")
    if params != None:
        url_params = urllib.urlencode(params)
        conn.request("GET", endpoint + "?" + url_params)
    else:
        conn.request("GET", endpoint)

    return conn.getresponse()

class TestHelpers(unittest.TestCase):
    def setUp(self):
        delete_db()

    def tearDown(self):
        delete_db()

    def test_register_user(self):
        helpers.register_user("ab", "1", "sam", "phippen", "samphippen@googlemail.com", "1")
        self.assertEqual(len(get_registrations()), 1)

    def test_register_many_users(self):
        n = random.randint(30, 100)
        for i in xrange(0,n):
            helpers.register_user("ab", "1", "sam", "phippen", "samphippen@googlemail.com", "1")
        self.assertEqual(len(get_registrations()), n)

if __name__ == '__main__':
    unittest.main()
