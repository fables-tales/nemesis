# -*- coding: UTF-8 -*-

import datetime
import httplib
import logging
import base64
import unittest
import urllib
import StringIO
import sys
import os

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common_test_helpers import apache_mode, delete_db, get_registrations, assert_no_emails, last_email, last_n_emails, remove_user, root, template

import helpers
from sqlitewrapper import PendingUser, PendingEmail, sqlite_connect

from libnemesis import srusers, User

def make_connection():
    if not apache_mode():
        return httplib.HTTPConnection("127.0.0.1",5000)
    else:
        return httplib.HTTPSConnection("localhost")

def modify_endpoint(endpoint):
    return "/userman" + endpoint if apache_mode() else endpoint

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
        u = srusers.user('old')
        if u.in_db:
            u.delete()

    def _exec(self, statement, arguments):
        conn = sqlite_connect()
        cur = conn.cursor()
        cur.execute(statement, arguments)
        conn.commit()

    def _make_old(self, table, username):
        old_time = datetime.datetime(2012, 01, 01).strftime('%Y-%m-%d %H:%M:%S')
        self._exec('UPDATE ' + table + ' SET request_time=? WHERE username=?', \
                        (old_time, username))

    def test_clear_old_emails(self):
        pe = PendingEmail('old')
        pe.new_email = 'old@srobo.org'
        pe.verify_code = 'bibble-old'
        pe.save()

        self._make_old('email_changes', 'old')

        pe = PendingEmail('abc')
        pe.new_email = 'nope@srobo.org'
        pe.verify_code = 'bibble-new'
        pe.save()

        helpers.clear_old_emails()

        pe = PendingEmail('old')
        assert not pe.in_db

        pe = PendingEmail('abc')
        assert pe.in_db

    def test_clear_old_registrations(self):
        first_name = 'old'
        last_name = 'user'
        old_user = srusers.user('old')
        old_user.cname = first_name
        old_user.sname = last_name
        old_user.email = ''
        old_user.save()

        old_team_leader = User('teacher_coll1')

        pu = PendingUser('old')
        pu.teacher_username = old_team_leader.username
        pu.college = 'college-1'
        pu.team = 'team-ABC'
        pu.email = 'nope@srobo.org'
        pu.verify_code = 'bibble-old'
        pu.save()

        self._make_old('registrations', 'old')

        pu = PendingUser('abc')
        pu.teacher_username = 'jim'
        pu.college = 'new-college-1'
        pu.team = 'team-NEW'
        pu.email = 'nope@srobo.org'
        pu.verify_code = 'bibble'
        pu.save()

        helpers.clear_old_registrations()

        pu = PendingUser('old')
        assert not pu.in_db

        pu = PendingUser('abc')
        assert pu.in_db

        ps = last_email()
        toaddr = ps.toaddr
        team_lead_email = old_team_leader.email
        assert toaddr == team_lead_email

        vars = ps.template_vars
        team_lead_first = old_team_leader.first_name
        assert team_lead_first == vars['name']
        assert first_name == vars['pu_first_name']
        assert last_name == vars['pu_last_name']

        template = ps.template_name
        assert template == 'registration_expired'

    def test_is_email_used_no(self):
        email = 'nope@srobo.org'
        used = helpers.email_used(email)
        assert used == False

    def test_is_email_used_full_user(self):
        email = 'sam4@example.com' # student_coll2_2
        used = helpers.email_used(email)
        assert used == True

    def test_is_email_used_pending_user(self):
        email = 'pu@srobo.org'
        pu = PendingUser('pu')
        pu.college = 'c'
        pu.team = 't'
        pu.teacher_username = 'tu'
        pu.verify_code = 'vc'
        pu.email = email
        pu.save()

        used = helpers.email_used(email)
        assert used == True

    def test_is_email_used_pending_email_change(self):
        email = 'pe@srobo.org'
        pe = PendingEmail('pu')
        pe.verify_code = 'vc'
        pe.new_email = email
        pe.save()

        used = helpers.email_used(email)
        assert used == True

class TestValidityHelpers(unittest.TestCase):
    def test_is_email_valid(self):
        valids = ['pe@srobo.org', 'a@b.cc', 'sam@example.com']
        invalids = ['@srobo.org', '@b.cc', 'a@b', 'a@.cc', 'a@b.', 'a@b.c', 'a@cc', 'bacon', 'bacon.cc']
        for email in valids:
            is_valid = helpers.is_email_valid(email)
            assert is_valid, email

        for email in invalids:
            is_valid = helpers.is_email_valid(email)
            assert not is_valid, email

    def test_is_name_valid(self):
        valids = ['valid name', 'Valid', "Lycée Emmanuel", "émmanuel", "Teal'c", u"\u5317\u4EB0", \
                  'th"at', 'spa(m', 'spa)m', 'spa&m', 'spa=m']
        invalids = ['@srobo', '2this', '"that', '(m', ')m', '&m', '=m']
        for name in valids:
            is_valid = helpers.is_name_valid(name)
            assert is_valid, name

        for name in invalids:
            is_valid = helpers.is_name_valid(name)
            assert not is_valid, name

class TestHelpersLogging(unittest.TestCase):

    def setUp(self):
        self._stream = StringIO.StringIO()
        defLoggger = logging.getLogger()
        self._handler = logging.StreamHandler(self._stream)
        defLoggger.addHandler(self._handler)
        defLoggger.setLevel(logging.NOTSET)

    def tearDown(self):
        defLoggger = logging.getLogger()
        defLoggger.removeHandler(self._handler)
        self._stream.close()

    def test_log_action(self):
        helpers.log_action('my-action', 'foo', bar = 'jam', spam = 'ham')
        logged = self._stream.getvalue()
        expected = "my-action: foo, bar: jam, spam: ham"
        assert expected in logged

    def test_log_action_objects(self):
        class Foo(object):
            def __repr__(self):
                return 'Foo(bacon)'

        helpers.log_action('action-my', Foo())
        logged = self._stream.getvalue()
        expected = "action-my: Foo(bacon)"
        assert expected in logged


if __name__ == '__main__':
    unittest.main()
