
import datetime
from nose.tools import with_setup
import json
import sys
import time
import unittest

import test_helpers

sys.path.append("../../nemesis")
import helpers
from sqlitewrapper import PendingUser

sys.path.append("../../nemesis/libnemesis")
from libnemesis import User, srusers

def create_pending_user(name = 'abc'):
    pu = PendingUser(name)
    pu.teacher_username = 'teacher_coll1'
    pu.college = 'college-1'
    pu.team = 'team-ABC'
    pu.email = name + '@srobo.org'
    pu.verify_code = 'bibble'

    return pu

@with_setup(test_helpers.delete_db)
def test_activate_needs_registration():
    r,data = test_helpers.server_get("/activate/nope/bees")
    status = r.status
    assert status == 404, data

@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_activate_wrong_code():
    pu = create_pending_user()
    pu.save()

    r,data = test_helpers.server_get("/activate/abc/bees")
    status = r.status
    assert status == 403, data

@with_setup(test_helpers.remove_user('1_ja1'), test_helpers.remove_user('1_ja1'))
@with_setup(test_helpers.delete_db, test_helpers.delete_db)
def test_activate_success():
    username = '1_ja1'

    rq_user = User.create_user("teacher_coll1", "facebees")
    cu = User.create_new_user(rq_user, 'college-1', 'James', 'Activate')
    assert cu.username == username

    pu = create_pending_user(username)
    pu.save()

    r,data = test_helpers.server_get("/activate/" + username + "/bibble")
    status = r.status
    assert status == 200, data

    u = User(username)
    email = u.email
    assert pu.email == email
    teams = [t.name for t in u.teams]
    assert pu.team in teams
    colleges = u.colleges
    assert pu.college in colleges

    students = srusers.group('students').members
    assert username in students

    pu = PendingUser(username)
    assert not pu.in_db, "registration DB entry should have been removed"

    # ensure we sent the team-leader a confirmation
    ps = test_helpers.last_email()
    toaddr = ps.toaddr
    tl_email = rq_user.email
    assert toaddr == tl_email

    vars = ps.template_vars
    tl_name = rq_user.first_name
    assert tl_name == vars['name']
    first_name = cu.first_name
    assert first_name == vars['au_first_name']
    last_name = cu.last_name
    assert last_name == vars['au_last_name']
    assert username == vars['au_username']

    template = ps.template_name
    assert template == 'user_activated_team_leader'
