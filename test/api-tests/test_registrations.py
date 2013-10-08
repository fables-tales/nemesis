
from nose.tools import with_setup
import sys

import test_helpers
from test_helpers import remove_user

sys.path.append("../../nemesis")
from sqlitewrapper import PendingUser

sys.path.append("../../nemesis/libnemesis")
from libnemesis import User

NEW_USER_FNAME = 'register'
NEW_USER_LNAME = 'this.user'

def test_registration_no_user():
    r,data = test_helpers.server_post("/registrations")
    assert r.status == 403

@with_setup(remove_user('1_rt1'), remove_user('1_rt1'))
@with_setup(test_helpers.delete_db, test_helpers.delete_db)
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
    assert status == 202, data

    created = User.create_user('1_rt1')
    assert created.email == ''

    pending = PendingUser('1_rt1')
    assert pending.email == "bob@example.com"
    assert pending.team == "team-ABC"
    assert pending.college == "college-1"

    email_datas = test_helpers.last_n_emails(2)

    student_ps = email_datas[0]
    template = student_ps.template_name
    assert template == 'new_user'
    to = student_ps.toaddr
    assert to == new_email
    vars = student_ps.template_vars
    assert NEW_USER_FNAME == vars['name']
    vcode = pending.verify_code
    assert vcode in vars['activation_url']

    teacher = User.create_user("teacher_coll1")

    teacher_ps = email_datas[1]
    template = teacher_ps.template_name
    assert template == 'user_requested'
    to = teacher_ps.toaddr
    assert to == teacher.email
    vars = teacher_ps.template_vars
    assert NEW_USER_FNAME == vars['pu_first_name']
    assert NEW_USER_LNAME == vars['pu_last_name']
    assert new_email == vars['pu_email']
    assert '1_rt1' == vars['pu_username']
    assert 'team-ABC' == vars['pu_team']
    assert 'college the first' == vars['pu_college']

    vars_str = teacher_ps.template_vars_json
    assert vcode not in vars_str, "Should not contain the verification code."

@with_setup(remove_user('1_rt1'), remove_user('1_rt1'))
@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_registration_rq_from_blueshirt():
    new_email = "bob@example.com"
    params = {"username":"blueshirt",
              "password":"blueshirt",
              "first_name":NEW_USER_FNAME,
              "last_name":NEW_USER_LNAME,
              "email":new_email,
              "team":"team-ABC",
              "college":"college-1"}

    r,data = test_helpers.server_post("/registrations", params)
    status = r.status
    assert status == 202, data

    created = User.create_user('1_rt1')
    assert created.email == ''

    pending = PendingUser('1_rt1')
    assert pending.email == "bob@example.com"
    assert pending.team == "team-ABC"
    assert pending.college == "college-1"

    email_datas = test_helpers.last_n_emails(2)

    student_ps = email_datas[0]
    template = student_ps.template_name
    assert template == 'new_user'
    to = student_ps.toaddr
    assert to == new_email
    vars = student_ps.template_vars
    assert NEW_USER_FNAME == vars['name']
    vcode = pending.verify_code
    assert vcode in vars['activation_url']

    teacher = User.create_user("blueshirt")

    teacher_ps = email_datas[1]
    template = teacher_ps.template_name
    assert template == 'user_requested'
    to = teacher_ps.toaddr
    assert to == teacher.email
    vars = teacher_ps.template_vars
    assert NEW_USER_FNAME == vars['pu_first_name']
    assert NEW_USER_LNAME == vars['pu_last_name']
    assert new_email == vars['pu_email']
    assert '1_rt1' == vars['pu_username']
    assert 'team-ABC' == vars['pu_team']
    assert 'college the first' == vars['pu_college']

    vars_str = teacher_ps.template_vars_json
    assert vcode not in vars_str, "Should not contain the verification code."

@with_setup(remove_user('2_rt1'), remove_user('2_rt1'))
@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_registration_wrong_college():
    params = {"username":"teacher_coll1",
              "password":"facebees",
              "first_name":NEW_USER_FNAME,
              "last_name":NEW_USER_LNAME,
              "email":"bob@example.com",
              "team":"team-ABC",
              "college":"college-2"}

    r,data = test_helpers.server_post("/registrations", params)

    status = r.status
    assert status == 403
    assert 'BAD_COLLEGE' in data
    assert len(test_helpers.get_registrations()) == 0
    test_helpers.delete_db()

def test_registration_not_authed():
    test_helpers.delete_db()

    params = {"username":"teacher_coll1",
              "first_name":"register",
              "last_name":"this.user",
              "email":"bob@example.com",
              "team":"team-ABC",
              "college":"college-1"}

    r,data = test_helpers.server_post("/registrations", params)
    status = r.status
    assert status == 403
    assert 'NO_PASSWORD' in data
    assert len(test_helpers.get_registrations()) == 0
    test_helpers.delete_db()

def test_registration_rq_from_student():
    test_helpers.delete_db()

    params = {"username":"student_coll1_1",
              "password":"cows",
              "first_name":"register",
              "last_name":"this.user",
              "email":"bob@example.com",
              "team":"team-ABC",
              "college":"college-1"}

    r,data = test_helpers.server_post("/registrations", params)
    status = r.status
    assert status == 403
    assert 'YOU_CANT_REGISTER_USERS' in data
    assert len(test_helpers.get_registrations()) == 0

    try:
        created = User.create_user('2_rt1')
        assert False, "Should not have created user"
    except:
        pass

    pending = PendingUser('2_rt1')
    assert not pending.in_db

    test_helpers.assert_no_emails()

@with_setup(remove_user('1_ss1'), remove_user('1_ss1'))
@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_registration_name_in_use():
    params = {"username":"teacher_coll1",
              "password":"facebees",
              "first_name":'student2', # student_coll1_2
              "last_name":'student',
              "email":"bob@example.com",
              "team":"team-ABC",
              "college":"college-1"}

    r,data = test_helpers.server_post("/registrations", params)

    status = r.status
    assert status == 403, data
    assert 'DETAILS_ALREADY_USED' in data
    assert len(test_helpers.get_registrations()) == 0

    try:
        created = User.create_user('1_ss1')
        assert False, "Should not have created user"
    except:
        pass

    pending = PendingUser('1_ss1')
    assert not pending.in_db

    test_helpers.assert_no_emails()

@with_setup(remove_user('1_rt1'), remove_user('1_rt1'))
@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_registration_email_in_use():
    params = {"username":"teacher_coll1",
              "password":"facebees",
              "first_name":NEW_USER_FNAME,
              "last_name":NEW_USER_LNAME,
              "email":"sam@sam2518.com", # student_coll2_2
              "team":"team-ABC",
              "college":"college-1"}

    r,data = test_helpers.server_post("/registrations", params)

    assert r.status == 403
    assert 'DETAILS_ALREADY_USED' in data
    assert len(test_helpers.get_registrations()) == 0

    try:
        created = User.create_user('1_rt1')
        assert False, "Should not have created user"
    except:
        pass

    pending = PendingUser('1_rt1')
    assert not pending.in_db

    test_helpers.assert_no_emails()
