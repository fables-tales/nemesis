
import datetime
import httplib
import base64
import unittest
import random
import urllib
import sys
import os
sys.path.insert(0,os.path.abspath('../../nemesis/'))
import helpers as helpers


def apache_mode():
    return os.path.exists(".apachetest")

def make_connection():
    if not apache_mode():
        return httplib.HTTPConnection("127.0.0.1",5000)
    else:
        return httplib.HTTPSConnection("localhost")

def modify_endpoint(endpoint):
    return "/userman" + endpoint if apache_mode() else endpoint

def delete_db():
    conn = helpers.sqlite_connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM registrations")
    cur.execute("DELETE FROM email_changes")
    conn.commit()

def get_registrations():
    conn = helpers.sqlite_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM registrations")
    return list(cur)

def unicode_encode(params_hash):
    for key in params_hash:
        params_hash[key] = params_hash[key].encode("utf-8")

def server_post(endpoint, params=None):
    conn = make_connection()
    endpoint = modify_endpoint(endpoint)
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}
    if params != None:
        if params.has_key("username") and params.has_key("password"):
            base64string = base64.encodestring('%s:%s' % (params["username"], params["password"])).replace('\n', '')
            headers["Authorization"] = "Basic %s" % base64string
            del params["username"]
            del params["password"]
        unicode_encode(params)
        url_params = urllib.urlencode(params)
        conn.request("POST", endpoint, url_params, headers)
    else:
        conn.request("POST", endpoint)

    resp = conn.getresponse()
    data = resp.read()
    return resp, data


def server_get(endpoint, params=None):
    conn = make_connection()
    endpoint = modify_endpoint(endpoint)
    headers = {}
    if params != None:
        if params.has_key("username") and params.has_key("password"):
            base64string = base64.encodestring('%s:%s' % (params["username"], params["password"])).replace('\n', '')
            headers["Authorization"] = "Basic %s" % base64string
            del params["username"]
            del params["password"]
        url_params = urllib.urlencode(params)
        conn.request("GET", endpoint, url_params, headers)
    else:
        conn.request("GET", endpoint)

    resp = conn.getresponse()
    data = resp.read()
    return resp, data

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

    def test_change_email_u(self):
        helpers.new_email('abc', 'nope@srobo.org', 'bibble')
        rq = helpers.get_change_email_request(username = 'abc')
        assert rq['username'] == 'abc'
        assert rq['new_email'] == 'nope@srobo.org'
        assert rq['verify_code'] == 'bibble'

    def test_re_change_email_u(self):
        helpers.new_email('abc', 'nope@srobo.org', 'bibble')
        helpers.new_email('abc', 'thing@srobo.org', 'bibble')

        rq = helpers.get_change_email_request(username = 'abc')
        assert rq['username'] == 'abc'
        assert rq['new_email'] == 'thing@srobo.org'
        assert rq['verify_code'] == 'bibble'

    def test_email_request_age(self):
        rq = { 'request_time': datetime.datetime.now() }
        is_valid = helpers.is_email_request_valid(rq)
        assert is_valid

        rq = { 'request_time': datetime.datetime.now() - datetime.timedelta(days = 4) }
        is_valid = helpers.is_email_request_valid(rq)
        assert not is_valid

    def test_remove_request(self):
        helpers.new_email('abc', 'abc@srobo.org', 'bibble1')
        helpers.new_email('def', 'def@srobo.org', 'bibble2')

        helpers.clear_new_email_request('abc')
        assert helpers.get_change_email_request(username = 'abc') is None
        assert helpers.get_change_email_request(username = 'def') is not None

if __name__ == '__main__':
    unittest.main()
