import test_helpers
import sys

sys.path.append("../../nemesis/libnemesis")
from libnemesis import User

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
    assert r.status == 403

def test_post_teacher_own_student():
    params = {"username":"teacher_coll1",
              "password":"facebees",
              }
    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200

def test_post_blueshirt_own_student():
    params = {"username":"blueshirt",
              "password":"blueshirt",
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200

def test_post_sets_email():
    old_email = User("student_coll1_1").email
    params = {"username":"blueshirt",
              "password":"blueshirt",
              "new_email":"new-emailexample.com",
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200
    assert User("student_coll1_1").email == "new-emailexample.com"

    u = User("student_coll1_1")
    u.set_email(old_email)
    u.save()

def test_post_sets_password():
    old_password = "cows"

    params = {"username":"blueshirt",
              "password":"blueshirt",
              "new_password":"com",
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200
    assert User("student_coll1_1")._user.bind("com")

    u = User("student_coll1_1")
    u.set_password(old_password)
    u.save()
