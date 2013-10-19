import json
import test_helpers
import sys

sys.path.append("../../nemesis/libnemesis")
from libnemesis import User

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

def test_user_get_blueshirt_wrong_password():
    params = {"username":"blueshirt",
              "password":"a",
              }

    r,data = test_helpers.server_get("/user/blueshirt", params)

    assert r.status == 403
