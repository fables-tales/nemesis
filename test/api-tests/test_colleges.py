import test_helpers
import json

def test_colleges_no_user():
    params = {}

    r,data = test_helpers.server_get("/colleges", params)

    assert r.status == 403

def test_colleges_blueshirt():
    params = {"username":"blueshirt",
              "password":"blueshirt"}

    r,data = test_helpers.server_get("/colleges", params)

    assert r.status == 200
    colleges = json.loads(data)

    assert colleges["colleges"][0] == "college-1"

def test_colleges_teacher_coll2():
    params = {"username":"teacher_coll2",
              "password":"noway"}

    r,data = test_helpers.server_get("/colleges", params)

    assert r.status == 200
    colleges = json.loads(data)

    assert colleges["colleges"][0] == "college-2"

