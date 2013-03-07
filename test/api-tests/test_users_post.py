import test_helpers

def test_post_no_user():
    r,data = test_helpers.server_post("/user/student_coll1_1")
    assert r.status == 403

def test_post_teacher_blueshirt():
    params = {"username":"teacher_coll1",
              "password":"facebees",
              }
    r,data = test_helpers.server_post("/user/blueshirt", params)
    assert r.status == 403

def test_post_other_teacher_blueshirt():
    params = {"username":"teacher_coll2",
              "password":"noway",
              }
    r,data = test_helpers.server_post("/user/blueshirt", params)

def test_post_teacher_own_student():
    params = {"username":"teacher_coll1",
              "password":"facebees",
              }
    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200
