
import datetime
from nose.tools import with_setup
import json
import sys
import time
import unittest

import test_helpers

sys.path.append("../../nemesis")
import helpers

sys.path.append("../../nemesis/libnemesis")
from libnemesis import User

@with_setup(test_helpers.clean_emails_and_db, test_helpers.remove_emails)
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

    template_lines = test_helpers.template('change_email.txt')

    email_data = test_helpers.last_email()
    assert email_data['subject'] in template_lines[0]
    assert email_data['toaddr'] == new_email
    msg = email_data['msg']
    assert user.first_name in msg
    assert '{url}' not in msg

    req_u = helpers.get_change_email_request(username = username)
    assert req_u is not None
    assert req_u['new_email'] == new_email

@with_setup(test_helpers.clean_emails_and_db, test_helpers.remove_emails)
def test_email_change_request_reset():
    """ Test that change requests via POST at /user/ are handled correclty. """
    username = "student_coll1_1"
    old_email = User(username).email
    new_email = "new-email@example.com"

    helpers.new_email(username, new_email, 'bees')

    params = {"username":"teacher_coll1",
              "password":"facebees",
              "new_email":old_email,
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200, data
    user = User(username)
    assert user.email == old_email

    all_mails = test_helpers.all_emails()
    assert len(all_mails) == 0

    req_u = helpers.get_change_email_request(username = username)
    assert req_u is None, 'POST using original email should have cleared request'

@with_setup(test_helpers.clean_emails_and_db, test_helpers.delete_db)
def test_email_changed_in_user_get():
    username = "student_coll1_1"
    new_email = 'nope@srobo.org'
    helpers.new_email(username, new_email, 'bees')

    params = {"username":username,
              "password":"cows"}
    r,data = test_helpers.server_get("/user/student_coll1_1", params)
    assert r.status == 200, data

    user_info = json.loads(data)
    user_new_email = user_info['new_email']

    assert user_new_email == new_email

@with_setup(test_helpers.clean_emails_and_db, test_helpers.delete_db)
def test_user_get_checks_same_email():
    username = "student_coll1_1"
    new_email = User(username).email
    helpers.new_email(username, new_email, 'bees')

    params = {"username":username,
              "password":"cows"}
    r,data = test_helpers.server_get("/user/student_coll1_1", params)
    assert r.status == 200, data

    user_info = json.loads(data)
    assert not user_info.has_key('new_email'), \
        "Should not have a new_email key when the new one and the current one match"

@with_setup(test_helpers.clean_emails_and_db)
def test_verify_needs_request():
    r,data = test_helpers.server_get("/verify/nope/bees")
    status = r.status
    assert status == 404, data

@with_setup(test_helpers.clean_emails_and_db, test_helpers.delete_db)
def test_verify_wrong_code():
    helpers.new_email('abc', 'nope@srobo.org', 'wrong')

    r,data = test_helpers.server_get("/verify/abc/bees")
    status = r.status
    assert status == 403, data

@with_setup(test_helpers.clean_emails_and_db, test_helpers.delete_db)
def test_verify_outdated_request():
    conn = helpers.sqlite_connect()
    cur = conn.cursor()
    statement = "INSERT INTO email_changes (username, new_email, request_time, verify_code) VALUES (?,?,?, ?)"
    old = datetime.datetime.now() - datetime.timedelta(days = 4)
    arguments = ('abc', 'nope@srobo.org', old.strftime('%Y-%m-%d %H:%M:%S'), 'bees')
    cur.execute(statement, arguments)
    conn.commit()

    r,data = test_helpers.server_get("/verify/abc/bees")
    status = r.status
    assert status == 410, data

@with_setup(test_helpers.clean_emails_and_db, test_helpers.delete_db)
def test_verify_success():
    username = "student_coll1_1"
    old_email = User(username).email
    new_email = "new-email@example.com"

    helpers.new_email('student_coll1_1', new_email, 'bees')

    r,data = test_helpers.server_get("/verify/" + username + "/bees")
    status = r.status
    assert status == 200, data

    u = User(username)
    email = u.email

    # restore the original first
    u.set_email(old_email)
    u.save()

    assert email == new_email
