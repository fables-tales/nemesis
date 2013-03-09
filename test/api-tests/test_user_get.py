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
