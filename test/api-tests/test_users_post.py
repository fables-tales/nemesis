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
    params = {"username":"teacher_coll1",
              "password":"facebees",
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

def test_post_sets_first_last_name():
    old_first = "student1i"
    old_last  = "student"

    params = {"username":"blueshirt",
              "password":"blueshirt",
              "new_first_name":"asdf",
              "new_last_name":"cheese",
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200
    details_dict = User("student_coll1_1").details_dictionary_for(User.create_user("student_coll1_1", "cows"))

    assert details_dict["first_name"] == "asdf"
    assert details_dict["last_name"] == "cheese"
    u = User("student_coll1_1")
    u.set_first_name(old_first)
    u.set_last_name(old_last)
    u.save()

def test_post_blueshirt_cant_set_team():
    old_team = "team-ABC"
    new_team = "team-DFE"

    params = {"username":"blueshirt",
              "password":"blueshirt",
              "new_team":new_team,
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200

    u = User("student_coll1_1")
    teams = [t.name for t in u.teams]
    assert [old_team] == teams

def test_post_teacher_sets_team():
    old_team = "team-ABC"
    new_team = "team-DFE"

    params = {"username":"teacher_coll1",
              "password":"facebees",
              "new_team":new_team,
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200

    u = User("student_coll1_1")
    teams = [t.name for t in u.teams]
    assert [new_team] == teams

    u.set_team(old_team)
    u.save()

def test_post_teacher_cant_set_nonexistent_team():
    old_team = "team-ABC"
    new_team = "team-PPP" # doesn't exist

    params = {"username":"teacher_coll1",
              "password":"facebees",
              "new_team":new_team,
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200

    u = User("student_coll1_1")
    teams = [t.name for t in u.teams]
    assert [old_team] == teams

def test_post_teacher_cant_set_other_team():
    old_team = "team-ABC"
    new_team = "team-QWZ" # exists, but this teacher doesn't own it

    params = {"username":"teacher_coll1",
              "password":"facebees",
              "new_team":new_team,
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200

    u = User("student_coll1_1")
    teams = [t.name for t in u.teams]
    assert [old_team] == teams
