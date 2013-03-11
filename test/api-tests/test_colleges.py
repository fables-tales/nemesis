import test_helpers
import json

def test_colleges_no_user():
    params = {}

    r,data = test_helpers.server_get("/colleges", params)

    print r,data
    assert r.status == 403

def test_colleges_no_password():
    params = {"username":"blueshirt"}
    r,data = test_helpers.server_get("/colleges", params)
    assert r.status == 403

def test_colleges_blueshirt():
    params = {"username":"blueshirt", "password":"blueshirt"}
    r,data = test_helpers.server_get("/colleges", params)
    print r.status
    print data
    assert r.status == 200
    assert len(json.loads(data)["colleges"]) == 2

def test_colleges_teacher_cant_access():
    params = {"username":"teacher_coll1", "password":"facebees"}
    r,data = test_helpers.server_get("/colleges", params)
    assert r.status == 403

def test_colleges_student_cant_access():
    params = {"username":"student_coll1_1", "password":"cows"}
    r,data = test_helpers.server_get("/colleges", params)
    assert r.status == 403
