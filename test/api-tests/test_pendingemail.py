
from datetime import timedelta
from nose.tools import raises, with_setup
import sys

import test_helpers

sys.path.append("../../nemesis")
from sqlitewrapper import *

@with_setup(test_helpers.delete_db)
def test_none_listed_at_start():
    all_list = PendingEmail.ListAll()
    assert len(all_list) == 0

@with_setup(test_helpers.delete_db)
def test_one_listed():
    test_creation()

    all_list = PendingEmail.ListAll()
    assert len(all_list) == 1

    pe = all_list[0]

    assert type(pe) == PendingEmail

    assert pe.in_db
    assert pe.username == 'abc'
    assert pe.new_email == 'nope@srobo.org'
    assert pe.verify_code == 'bibble'

@with_setup(test_helpers.delete_db)
def test_none_listed_after_removal():
    test_creation()

    all_list = PendingEmail.ListAll()
    for pu in all_list:
        pu.delete()

    all_list = PendingEmail.ListAll()
    assert len(all_list) == 0

@with_setup(test_helpers.delete_db)
def test_empty_at_start():
    pe = PendingEmail('abc')
    assert pe.in_db == False
    assert pe.new_email is None
    assert pe.verify_code is None
    assert pe.age == timedelta()

def test_properties():
    pe = PendingEmail('abc')
    pe.new_email = 'nope@srobo.org'
    pe.verify_code = 'bibble'

    assert pe.username == 'abc'
    assert pe.new_email == 'nope@srobo.org'
    assert pe.verify_code == 'bibble'

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_creation():
    pe = PendingEmail('abc')
    pe.new_email = 'nope@srobo.org'
    pe.verify_code = 'bibble'

    pe.save()
    assert pe.in_db

    pe = PendingEmail('abc')
    assert pe.in_db
    assert pe.username == 'abc'
    assert pe.new_email == 'nope@srobo.org'
    assert pe.verify_code == 'bibble'
    age = pe.age
    assert age > timedelta()
    assert age < timedelta(minutes = 1)

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_update():
    test_creation()
    new_email = 'bees@srobo.org'

    pe = PendingEmail('abc')
    pe.new_email = new_email
    pe.save()

    pe = PendingEmail('abc')
    assert pe.new_email == new_email

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_delete():
    test_creation()

    pe = PendingEmail('abc')
    pe.delete()
    assert not pe.in_db

    pe = PendingEmail('abc')
    assert not pe.in_db

@with_setup(test_helpers.remove_emails, test_helpers.remove_emails)
def test_send_email():
    first_name = 'jim'
    verification_url = 'http://verify'
    new_email = 'new_email@nope.sr'
    pe = PendingEmail('abc')
    pe.new_email = new_email
    pe.send_verification_email(first_name, verification_url)

    last_email = test_helpers.last_email()

    message = last_email['msg']
    assert first_name in message
    assert verification_url in message
    assert new_email == last_email['toaddr']

    template_lines = test_helpers.template('change_email.txt')
    subject_line = template_lines[0]
    assert last_email['subject'] in subject_line

@raises(AttributeError)
def test_invalid_property():
    pe = PendingEmail('abc')
    print pe.bacon
