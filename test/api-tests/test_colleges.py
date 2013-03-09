import test_helpers
import json

def test_colleges_no_user():
    params = {}

    r,data = test_helpers.server_get("/colleges", params)

    assert r.status == 200
    assert len(json.loads(data)["colleges"]) == 2
