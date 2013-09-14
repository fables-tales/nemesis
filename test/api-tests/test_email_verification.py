
import datetime
import glob
from nose.tools import with_setup
import json
import os.path
import sys
import time
import unittest

import test_helpers

sys.path.append("../../nemesis")
import helpers

sys.path.append("../../nemesis/libnemesis")
from libnemesis import User

def setUp():
    if test_helpers.apache_mode():
        # Can't run these tests if the web server isn't local
        raise unittest.SkipTest
    else:
        remove_emails()
        test_helpers.delete_db

def remove_emails():
    for f in all_emails():
        os.remove(f)

def root():
   root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
   return root

def all_emails():
    pattern = os.path.join(root(), 'nemesis/mail-*.sent-mail')
    files = glob.glob(pattern)
    return files

def last_email():
    files = all_emails()
    assert len(files) == 1
    with open(files[0], 'r') as f:
        mail_data = json.load(f)
        return mail_data

def template(name):
    file_path = os.path.join(root(), 'nemesis/templates', name)
    with open(file_path, 'r') as f:
        return f.readlines()

@with_setup(setUp, remove_emails)
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

    template_lines = template('change_email.txt')

    email_data = last_email()
    assert email_data['subject'] in template_lines[0]
    assert email_data['toaddr'] == new_email
    msg = email_data['msg']
    assert user.first_name in msg
    assert '{url}' not in msg

    req_u = helpers.get_change_email_request(username = username)
    assert req_u is not None
    assert req_u['new_email'] == new_email

    req_e = helpers.get_change_email_request(new_email = new_email)
    assert req_e is not None
    assert req_e['username'] == username

@with_setup(setUp, remove_emails)
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

    all_mails = all_emails()
    assert len(all_mails) == 0

    req_u = helpers.get_change_email_request(username = username)
    assert req_u is None, 'POST using original email should have cleared request'

@with_setup(setUp, test_helpers.delete_db)
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

@with_setup(setUp)
def test_verify_needs_request():
    r,data = test_helpers.server_get("/verify/nope@srobo.org/bees")
    status = r.status
    assert status == 404, data

@with_setup(setUp, test_helpers.delete_db)
def test_verify_wrong_code():
    helpers.new_email('abc', 'nope@srobo.org', 'wrong')

    r,data = test_helpers.server_get("/verify/nope@srobo.org/bees")
    status = r.status
    assert status == 403, data

@with_setup(setUp, test_helpers.delete_db)
def test_verify_outdated_request():
    conn = helpers.sqlite_connect()
    cur = conn.cursor()
    statement = "INSERT INTO email_changes (username, new_email, request_time, verify_code) VALUES (?,?,?, ?)"
    old = datetime.datetime.now() - datetime.timedelta(days = 4)
    arguments = ('abc', 'nope@srobo.org', old.strftime('%Y-%m-%d %H:%M:%S'), 'bees')
    cur.execute(statement, arguments)
    conn.commit()

    r,data = test_helpers.server_get("/verify/nope@srobo.org/bees")
    status = r.status
    assert status == 410, data

@with_setup(setUp, test_helpers.delete_db)
def test_verify_success():
    username = "student_coll1_1"
    old_email = User(username).email
    new_email = "new-email@example.com"

    helpers.new_email('student_coll1_1', new_email, 'bees')

    r,data = test_helpers.server_get("/verify/" + new_email + "/bees")
    status = r.status
    assert status == 200, data

    u = User(username)
    email = u.email

    # restore the original first
    u.set_email(old_email)
    u.save()

    assert email == new_email
