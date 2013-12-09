
from datetime import timedelta
from nose.tools import raises, with_setup
import sys

import test_helpers

sys.path.append("../../nemesis")
from sqlitewrapper import *

@with_setup(test_helpers.delete_db)
def test_none_listed_at_start():
    all_list = PendingUser.ListAll()
    assert len(all_list) == 0

@with_setup(test_helpers.delete_db)
def test_one_listed():
    test_creation()

    all_list = PendingUser.ListAll()
    assert len(all_list) == 1

    pu = all_list[0]

    assert type(pu) == PendingUser

    assert pu.in_db
    assert pu.username == 'abc'
    assert pu.teacher_username == 'jim'
    assert pu.college == 'college-1'
    assert pu.team == 'team-ABC'
    assert pu.email == 'nope@srobo.org'
    assert pu.verify_code == 'bibble'

@with_setup(test_helpers.delete_db)
def test_none_listed_after_removal():
    test_creation()

    all_list = PendingUser.ListAll()
    for pu in all_list:
        pu.delete()

    all_list = PendingUser.ListAll()
    assert len(all_list) == 0

@with_setup(test_helpers.delete_db)
def test_empty_at_start():
    pu = PendingUser('abc')
    assert pu.in_db == False
    assert pu.teacher_username is None
    assert pu.college is None
    assert pu.email is None
    assert pu.team is None
    assert pu.verify_code is None

def test_properties():
    pu = PendingUser('abc')
    pu.teacher_username = 'jim'
    pu.college = 'college-1'
    pu.team = 'team-ABC'
    pu.email = 'nope@srobo.org'
    pu.verify_code = 'bibble'

    assert pu.username == 'abc'
    assert pu.teacher_username == 'jim'
    assert pu.college == 'college-1'
    assert pu.team == 'team-ABC'
    assert pu.email == 'nope@srobo.org'
    assert pu.verify_code == 'bibble'
    assert pu.age == timedelta()

def test_str():
    pu = PendingUser('abc')
    pu.teacher_username = 'jim'
    pu.college = 'college-1'
    pu.team = 'team-ABC'
    pu.email = 'nope@srobo.org'
    pu.verify_code = 'bibble'

    as_str = str(pu)
    assert 'PendingUser' in as_str
    assert 'abc' in as_str
    assert 'jim' in as_str
    assert 'college-1' in as_str
    assert 'team-ABC' in as_str
    assert 'nope@srobo.org' in as_str
    assert 'bibble' in as_str

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_creation():
    pu = PendingUser('abc')
    pu.teacher_username = 'jim'
    pu.college = 'college-1'
    pu.team = 'team-ABC'
    pu.email = 'nope@srobo.org'
    pu.verify_code = 'bibble'

    pu.save()
    assert pu.in_db

    pu = PendingUser('abc')
    assert pu.in_db
    assert pu.username == 'abc'
    assert pu.teacher_username == 'jim'
    assert pu.college == 'college-1'
    assert pu.team == 'team-ABC'
    assert pu.email == 'nope@srobo.org'
    assert pu.verify_code == 'bibble'
    assert pu.age > timedelta()
    assert pu.age < timedelta(minutes = 1)

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_update():
    test_creation()
    new_team = 'team-XYZ'

    pu = PendingUser('abc')
    pu.team = new_team
    pu.save()

    pu = PendingUser('abc')
    assert pu.team == new_team

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_delete():
    test_creation()

    pu = PendingUser('abc')
    pu.delete()
    assert not pu.in_db

    pu = PendingUser('abc')
    assert not pu.in_db

@raises(AttributeError)
def test_invalid_property():
    pu = PendingUser('abc')
    print pu.bacon
