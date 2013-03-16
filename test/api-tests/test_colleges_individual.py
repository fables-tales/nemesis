import test_helpers
import json

def test_college_no_user():
    params = {}
    r, data = test_helpers.server_get("/colleges/college-1", params)
    data = json.loads(data)

    assert r.status == 403

def test_college_valid_user():
    params = {"username":"student_coll1_1",
              "password":"cows"}

    r, data = test_helpers.server_get("/colleges/college-1", params)

    assert r.status == 200

    resp = json.loads(data)
    assert resp["name"] == "college the first"
    assert len(resp["users"]) == 1
    assert resp["users"][0] == "student_coll1_1"
    assert len(resp["teams"]) == 2
    assert sorted(resp["teams"]) == sorted(["team-ABC", "team-DFE"])

def test_college_403_bad_creds():
    params = {"username":"student_coll1_1",
              "password":"thisiswrong"}

    r, data = test_helpers.server_get("/colleges/college-1", params)

    assert r.status == 403

def test_college_teacher_cant_see_blueshirt():

    params = {"username":"teacher_coll1",
              "password":"facebees"}

    r, data = test_helpers.server_get("/colleges/college-1", params)

    assert r.status == 200

    resp = json.loads(data)
    assert resp["name"] == "college the first"
    assert "blueshirt" not in set(resp["users"])

def test_college_teacher_can_see_students_and_self():
    params = {"username":"teacher_coll1",
              "password":"facebees"}

    r, data = test_helpers.server_get("/colleges/college-1", params)

    assert r.status == 200

    resp = json.loads(data)
    assert resp["name"] == "college the first"
    assert "teacher_coll1" in set(resp["users"])
    assert "student_coll1_1" in set(resp["users"])
    assert "student_coll1_2" in set(resp["users"])

def test_college_blueshirt_can_see_any_college():
    params = {"username":"blueshirt",
              "password":"blueshirt"}

    r, data = test_helpers.server_get("/colleges/college-2", params)

    assert r.status == 200
    resp = json.loads(data)
    assert "users" not in resp.keys()
