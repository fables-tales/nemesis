
import datetime
from nose.tools import with_setup
import json
import sys
import time
import unittest

import test_helpers

sys.path.append("../../nemesis")
from sqlitewrapper import PendingEmail, sqlite_connect

sys.path.append("../../nemesis/libnemesis")
from libnemesis import User

def setup_new_email(username, new_email, verify_code):
    pe = PendingEmail(username)
    pe.new_email = new_email
    pe.verify_code = verify_code
    pe.save()

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_email_change_request():
    """ Test that change requests via POST at /user/ are handled correclty. """
    username = "student_coll1_1"
    old_email = User(username).email
    new_email = "new-email@example.com"
    params = {"username":"teacher_coll1",
              "password":"facebees",
              "new_email":new_email,
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200, data
    user = User(username)
    assert user.email == old_email

    ps = test_helpers.last_email()
    toaddr = ps.toaddr
    assert toaddr == new_email

    vars = ps.template_vars
    first_name = user.first_name
    assert first_name == vars['name']

    template = ps.template_name
    assert template == 'change_email'

    pe = PendingEmail(username)
    assert pe.in_db
    assert pe.new_email == new_email

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_email_change_request_reset():
    """ Test that change requests via POST at /user/ are handled correclty. """
    username = "student_coll1_1"
    old_email = User(username).email
    new_email = "new-email@example.com"
    setup_new_email(username, new_email, 'bees')

    params = {"username":"teacher_coll1",
              "password":"facebees",
              "new_email":old_email,
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200, data
    user = User(username)
    assert user.email == old_email

    pe = PendingEmail(username)
    assert not pe.in_db, 'POST using original email should have cleared request'

    test_helpers.assert_no_emails()

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_email_change_request_reset_without_change():
    """ Test that a change requests to the original value,
        where there is no actual outstanding request doens't explode"""
    username = "student_coll1_1"
    old_email = User(username).email

    params = {"username":"teacher_coll1",
              "password":"facebees",
              "new_email":old_email,
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200, data
    user = User(username)
    assert user.email == old_email

    test_helpers.assert_no_emails()

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_email_change_request_reset_without_change():
    """ Test that a change requests to the original value,
        where there is no actual outstanding request doens't explode"""
    username = "student_coll1_1"
    old_email = User(username).email

    params = {"username":"teacher_coll1",
              "password":"facebees",
              "new_email":old_email,
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200, data
    user = User(username)
    assert user.email == old_email

    test_helpers.assert_no_emails()

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_email_changed_in_user_get():
    username = "student_coll1_1"
    new_email = 'nope@srobo.org'
    setup_new_email(username, new_email, 'bees')

    params = {"username":username,
              "password":"cows"}
    r,data = test_helpers.server_get("/user/student_coll1_1", params)
    assert r.status == 200, data

    user_info = json.loads(data)
    user_new_email = user_info['new_email']

    assert user_new_email == new_email

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_email_changed_in_user_get_wrong_case():
    """
    Tests that when the user is requested with the wrong case,
    we still return the correct information about their pending email.
    """
    new_email = 'nope@srobo.org'
    setup_new_email("student_coll1_1", new_email, 'bees')

    params = {"username":"Student_Coll1_1",
              "password":"cows"}
    r,data = test_helpers.server_get("/user/Student_Coll1_1", params)
    assert r.status == 200, data

    user_info = json.loads(data)
    user_new_email = user_info['new_email']

    assert user_new_email == new_email

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_user_get_checks_same_email():
    username = "student_coll1_1"
    new_email = User(username).email
    setup_new_email(username, new_email, 'bees')

    params = {"username":username,
              "password":"cows"}
    r,data = test_helpers.server_get("/user/student_coll1_1", params)
    assert r.status == 200, data

    user_info = json.loads(data)
    assert not user_info.has_key('new_email'), \
        "Should not have a new_email key when the new one and the current one match"

@with_setup(test_helpers.delete_db)
def test_verify_needs_request():
    r,data = test_helpers.server_get("/verify/nope/bees")
    status = r.status
    assert status == 404, data

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_verify_wrong_code():
    setup_new_email('abc', 'nope@srobo.org', 'wrong')

    r,data = test_helpers.server_get("/verify/abc/bees")
    status = r.status
    assert status == 403, data

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_verify_outdated_request():
    conn = sqlite_connect()
    cur = conn.cursor()
    statement = "INSERT INTO email_changes (username, new_email, request_time, verify_code) VALUES (?,?,?, ?)"
    old = datetime.datetime.now() - datetime.timedelta(days = 4)
    arguments = ('abc', 'nope@srobo.org', old.strftime('%Y-%m-%d %H:%M:%S'), 'bees')
    cur.execute(statement, arguments)
    conn.commit()

    r,data = test_helpers.server_get("/verify/abc/bees")
    status = r.status
    assert status == 410, data

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_verify_success():
    username = "student_coll1_1"
    old_email = User(username).email
    new_email = "new-email@example.com"

    setup_new_email('student_coll1_1', new_email, 'bees')

    r,data = test_helpers.server_get("/verify/" + username + "/bees")
    status = r.status
    assert status == 200, data

    u = User(username)
    email = u.email

    # restore the original first
    u.set_email(old_email)
    u.save()

    assert email == new_email
