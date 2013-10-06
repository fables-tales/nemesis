
from datetime import datetime, timedelta
from nose.tools import raises, with_setup
import sys

import test_helpers

sys.path.append("../../nemesis")
from sqlitewrapper import *

def test_simple_properties():
    ps = PendingSend('abc')
    ps.toaddr = 'jim@srobo.org'
    ps.template_name = 'template-1'
    ps.last_error = 'bacon'

    assert ps.toaddr == 'jim@srobo.org'
    assert ps.template_name == 'template-1'
    assert ps.last_error == 'bacon'

def test_template_vars_property():
    print 'bacon'
    ps = PendingSend('abc')
    assert ps.template_vars is None

    ps.template_vars = {"foo": 'bar'}
    assert ps.template_vars == {'foo': 'bar'}

def test_retried():
    ps = PendingSend('abc')
    ps.toaddr = 'jim@srobo.org'
    assert ps.retry_count == 0

    ps.retried()
    ps.retried()
    ps.retried()

    assert ps.retry_count == 3

def test_sent():
    ps = PendingSend('abc')
    ps.toaddr = 'jim@srobo.org'
    assert ps.sent_time is None

    then = datetime.now() - timedelta(seconds = 2)
    ps.mark_sent()

    sent_time = ps.sent_time
    assert sent_time > then
    assert ps.is_sent

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_creation():
    ps = PendingSend()
    ps.toaddr = 'jim@srobo.org'
    ps.template_name = 'template-1'
    ps.template_vars = {"foo": 'bar'}
    ps.last_error = 'bacon'

    assert ps.id is None
    ps.save()
    assert ps.in_db
    assert ps.id > 0

    ps = PendingSend(ps.id)
    assert ps.in_db
    assert ps.toaddr == 'jim@srobo.org'
    assert ps.template_name == 'template-1'
    assert ps.template_vars == {'foo': 'bar'}
    assert ps.last_error == 'bacon'
    assert ps.retry_count == 0
    assert ps.age > timedelta()
    assert ps.age < timedelta(minutes = 1)

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_unsent_none():
    unsent = list(PendingSend.Unsent())
    assert len(unsent) == 0

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_unsent_one():
    ps = PendingSend()
    ps.toaddr = 'bob@srobo.org'
    ps.template_name = 'template-1'
    ps.template_vars = {"foo": 'bar'}
    ps.save()

    unsent = list(PendingSend.Unsent())
    assert len(unsent) == 1
    ps = unsent[0]
    toaddr = ps.toaddr
    assert toaddr == 'bob@srobo.org'

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_unsent_and_sent():
    ps = PendingSend()
    ps.toaddr = 'alice@srobo.org'
    ps.template_name = 'template-1'
    ps.template_vars = {"foo": 'bar'}
    ps.mark_sent()
    ps.save()

    ps = PendingSend()
    ps.toaddr = 'bob@srobo.org'
    ps.template_name = 'template-1'
    ps.template_vars = {"foo": 'bar'}
    ps.save()

    unsent = list(PendingSend.Unsent())
    assert len(unsent) == 1
    ps = unsent[0]
    toaddr = ps.toaddr
    assert toaddr == 'bob@srobo.org'

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_unsent_with_retries():
    ps = PendingSend()
    ps.toaddr = 'alice@srobo.org'
    ps.template_name = 'template-1'
    ps.template_vars = {"foo": 'bar'}
    ps.retry_count = 5
    ps.save()

    ps = PendingSend()
    ps.toaddr = 'bob@srobo.org'
    ps.template_name = 'template-1'
    ps.template_vars = {"foo": 'bar'}
    ps.save()

    unsent = list(PendingSend.Unsent())
    assert len(unsent) == 1
    ps = unsent[0]
    toaddr = ps.toaddr
    assert toaddr == 'bob@srobo.org'
