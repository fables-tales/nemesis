
from nose.tools import with_setup
import os
from unittest import TestCase

import test_helpers
from test_helpers import last_email

import mailer
from sqlitewrapper import PendingSend

# cache the original, since we'll be injecting a mock
# not sure why I couldn't do this as a class thing, but this seems to work.
orig_send_mail = mailer.send_email

class TestMailer(TestCase):
    @classmethod
    def tearDownClass(cls):
        mailer.send_email = orig_send_mail

    def setUp(self):
        test_helpers.delete_db()
        self.fake_send_email(None, None, None)
        mailer.send_email = self.fake_send_email

    def tearDown(self):
        test_helpers.delete_db()

    def fake_send_email(self, to, subject, msg):
        self._to = to
        self._subject = subject
        self._msg = msg

    def test_store_temaplate(self):
        exp_addr = 'a@b.cc'
        exp_tpl  = 'tpl'
        exp_vars = {'foo':'bar'}
        ps = mailer.store_template(exp_addr, exp_tpl, exp_vars)

        assert ps.in_db

        stored = last_email()
        toaddr = stored.toaddr
        assert exp_addr == toaddr
        tpl = stored.template_name
        assert exp_tpl == tpl
        vars = stored.template_vars
        assert exp_vars == vars

    def test_try_send_ok(self):
        exp_addr = 'a@b.cc'
        exp_tpl  = 'example'
        exp_vars = {'foo':'bar'}

        ps = PendingSend()
        ps.toaddr = exp_addr
        ps.template_name = exp_tpl
        ps.template_vars = exp_vars

        mailer.try_send(ps)

        tpl_lines = test_helpers.template(exp_tpl + '.txt')
        exp_subject = tpl_lines[0]

        assert exp_addr == self._to
        assert self._subject in exp_subject
        assert 'foo' not in self._msg
        assert 'bar' in self._msg

        ps_stored = PendingSend(ps.id)

        sent = ps_stored.is_sent
        assert sent

    def test_try_send_throws(self):
        exp_addr = 'a@b.cc'
        exp_tpl  = 'example'
        exp_vars = {'foo':'bar'}

        ps = PendingSend()
        ps.toaddr = exp_addr
        ps.template_name = exp_tpl
        ps.template_vars = exp_vars

        exc_msg = "I am a teapot"
        def throws(to, subject, msg):
            raise Exception(exc_msg)

        mailer.send_email = throws
        mailer.try_send(ps)

        ps_stored = PendingSend(ps.id)

        sent = ps_stored.is_sent
        assert not sent
        last_error = ps_stored.last_error
        assert exc_msg in last_error
        retries = ps_stored.retry_count
        assert 1 == retries
