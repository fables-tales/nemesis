
from nose.tools import with_setup
import sys

import test_helpers

sys.path.append("../../nemesis")
from sqlitewrapper import PendingUser

sys.path.append("../../nemesis/libnemesis")
from libnemesis import User, srusers

NEW_USER_FNAME = 'register'
NEW_USER_LNAME = 'this.user'

def setUp():
    test_helpers.remove_emails()
    test_helpers.delete_db()

def remove_user(name):
    def helper():
        u = srusers.user(name)
        if u.in_db:
            u.delete()
    return helper

def test_registration_no_user():
    r,data = test_helpers.server_post("/registrations")
    assert r.status == 403

@with_setup(remove_user('1_rt1'), remove_user('1_rt1'))
@with_setup(setUp, test_helpers.remove_emails)
def test_registration_user_and_form():
    new_email = "bob@example.com"
    params = {"username":"teacher_coll1",
              "password":"facebees",
              "first_name":NEW_USER_FNAME,
              "last_name":NEW_USER_LNAME,
              "email":new_email,
              "team":"team-ABC",
              "college":"college-1"}

    r,data = test_helpers.server_post("/registrations", params)
    status = r.status
    assert status == 202

    created = User.create_user('1_rt1')
    assert created.email == ''

    pending = PendingUser('1_rt1')
    assert pending.email == "bob@example.com"
    assert pending.team == "team-ABC"
    assert pending.college == "college-1"

    template_lines = test_helpers.template('new_user.txt')

    email_data = test_helpers.last_email()
    assert email_data['subject'] in template_lines[0]
    assert email_data['toaddr'] == new_email
    msg = email_data['msg']
    assert NEW_USER_FNAME in msg
    assert '{activate_url}' not in msg
    vcode = pending.verify_code
    assert vcode in msg

@with_setup(remove_user('2_rt1'), remove_user('2_rt1'))
@with_setup(setUp, test_helpers.remove_emails)
def test_registration_wrong_college():
    params = {"username":"teacher_coll1",
              "password":"facebees",
              "first_name":NEW_USER_FNAME,
              "last_name":NEW_USER_LNAME,
              "email":"bob@example.com",
              "team":"team-ABC",
              "college":"college-2"}

    r,data = test_helpers.server_post("/registrations", params)
    assert r.status == 403
    assert len(test_helpers.get_registrations()) == 0

    try:
        created = User.create_user('2_rt1')
        assert False, "Should not have created user"
    except:
        pass

    pending = PendingUser('2_rt1')
    assert not pending.in_db

    mails = test_helpers.all_emails()
    assert len(mails) == 0
