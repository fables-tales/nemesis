
import json
from nose.tools import with_setup
import sys

import test_helpers

sys.path.append("../../nemesis/libnemesis")
from libnemesis import User, srusers

def test_user_get_no_user():
    params = {}
    r,data = test_helpers.server_get("/user/student_coll1_1", params)
    assert r.status == 403

def test_user_get_wrong_user():
    params = {"username":"teacher_coll2",
              "password":"noway",
              }

    r,data = test_helpers.server_get("/user/student_coll1_1", params)
    assert r.status == 403

def test_user_get_self():
    params = {"username":"student_coll1_1",
              "password":"cows"}
    r,data = test_helpers.server_get("/user/student_coll1_1", params)
    assert r.status == 200
    assert data.find("student_coll1_1") != -1

def test_user_get_self_wrong_case():
    """
    Tests that when a user auths with the wrong case,
    and requests the wrong case of username in the url,
    we still respond with the correctly cased data.
    """
    params = {"username":"Student_Coll1_1",
              "password":"cows"}
    r,data = test_helpers.server_get("/user/studenT_coll1_1", params)
    assert r.status == 200
    assert data.find("student_coll1_1") != -1

def test_user_get_other_can_view():
    params = {"username":"blueshirt",
              "password":"blueshirt",
              }

    r,data = test_helpers.server_get("/user/student_coll1_1", params)
    assert r.status == 200
    assert data.find("student_coll1_1") != -1

def test_user_colleges():
    params = {"username":"blueshirt",
              "password":"blueshirt",
              }

    r,data = test_helpers.server_get("/user/blueshirt", params)
    data = json.loads(data)

    assert r.status == 200
    assert "college-1" in data[u"colleges"]

def test_user_teams():
    params = {"username":"student_coll1_1",
              "password":"cows",
              }

    r,data = test_helpers.server_get("/user/student_coll1_1", params)
    data = json.loads(data)

    assert r.status == 200
    assert ["team-ABC"] == data[u"teams"]

def test_user_properties_blueshirt():
    params = {"username":"blueshirt",
              "password":"blueshirt",
              }

    r,data = test_helpers.server_get("/user/blueshirt", params)
    data = json.loads(data)

    assert r.status == 200
    assert data['is_blueshirt']
    assert not data['is_student']
    assert not data['is_team_leader']

def test_user_properties_student():
    params = {"username":"student_coll1_1",
              "password":"cows",
              }

    r,data = test_helpers.server_get("/user/student_coll1_1", params)
    data = json.loads(data)

    assert r.status == 200
    assert data['is_student']
    assert not data['is_team_leader']
    assert not data['is_blueshirt']

def test_user_properties_teacher():
    params = {"username":"teacher_coll2",
              "password":"noway",
              }

    r,data = test_helpers.server_get("/user/teacher_coll2", params)
    data = json.loads(data)

    assert r.status == 200
    assert data['is_team_leader']
    assert not data['is_student']
    assert not data['is_blueshirt']

def test_user_media_consent_false():
    params = {"username":"teacher_coll2",
              "password":"noway",
              }

    r,data = test_helpers.server_get("/user/teacher_coll2", params)
    data = json.loads(data)

    assert r.status == 200
    assert not data['has_media_consent']

@with_setup(test_helpers.remove_user('to-consent'), test_helpers.remove_user('to-consent'))
def test_user_media_consent_true():
    username = 'to-consent'
    sru = srusers.user(username)
    sru.cname = 'to'
    sru.sname = 'consent'
    sru.email = ''
    sru.save()
    for gid in ['students', 'media-consent', 'college-2']:
        g = srusers.group(gid)
        g.user_add(sru)
        g.save()

    params = {"username":"teacher_coll2",
              "password":"noway",
              }

    r,data = test_helpers.server_get("/user/to-consent", params)
    data = json.loads(data)

    assert r.status == 200
    assert data['has_media_consent']

def test_user_withdrawn_false():
    params = {"username":"teacher_coll2",
              "password":"noway",
              }

    r,data = test_helpers.server_get("/user/teacher_coll2", params)
    data = json.loads(data)

    assert r.status == 200
    assert not data['has_withdrawn']

@with_setup(test_helpers.remove_user('to-withdraw'), test_helpers.remove_user('to-withdraw'))
def test_user_withdrawn_true():
    username = 'to-withdraw'
    sru = srusers.user(username)
    sru.cname = 'to'
    sru.sname = 'consent'
    sru.email = ''
    sru.save()
    for gid in ['students', 'withdrawn', 'college-2']:
        g = srusers.group(gid)
        g.user_add(sru)
        g.save()

    params = {"username":"teacher_coll2",
              "password":"noway",
              }

    r,data = test_helpers.server_get("/user/to-withdraw", params)
    data = json.loads(data)

    assert r.status == 200
    assert data['has_withdrawn']

def test_user_get_blueshirt_wrong_password():
    params = {"username":"blueshirt",
              "password":"a",
              }

    r,data = test_helpers.server_get("/user/blueshirt", params)

    assert r.status == 403
