from nose.tools import with_setup
import test_helpers
import sys

sys.path.append("../../nemesis/libnemesis")
from libnemesis import User, srusers

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

def test_post_teacher_other_student():
    params = {"username":"teacher_coll2",
              "password":"noway",
              }
    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    status = r.status
    assert status == 403

def test_post_blueshirt_own_student():
    params = {"username":"blueshirt",
              "password":"blueshirt",
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200

def test_post_sets_others_password():
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

def test_post_sets_own_password():
    old_password = "blueshirt"
    new_password = 'bacon'

    params = {"username":"blueshirt",
              "password":old_password,
              "new_password":new_password,
              }

    r,data = test_helpers.server_post("/user/blueshirt", params)
    assert r.status == 200
    assert User("blueshirt")._user.bind(new_password)

    u = User("blueshirt")
    u.set_password(old_password)
    u.save()

def test_post_sets_own_password_and_name():
    old_password = "blueshirt"
    new_password = 'bacon'
    old_first = "Blue"
    old_last  = "Shirt"

    params = {"username":"blueshirt",
              "password":old_password,
              "new_password":new_password,
              "new_first_name":'new_first',
              "new_last_name":'new_last',
              }

    r,data = test_helpers.server_post("/user/blueshirt", params)
    assert r.status == 200
    assert User("blueshirt")._user.bind(new_password)

    u = User("blueshirt")
    first = u.first_name
    last = u.last_name
    u.set_password(old_password)
    u.set_first_name(old_first)
    u.set_last_name(old_last)
    u.save()

    assert first == 'new_first'
    assert last == 'new_last'

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

def test_post_doesnt_set_blank_first_name():
    old_first = User("student_coll1_1").first_name
    params = {"username":"student_coll1_1",
              "password":"cows",
              "new_first_name":"",
              }

    r, data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200
    assert User("student_coll1_1").first_name == old_first

def test_post_doesnt_set_blank_last_name():
    old_last = User("student_coll1_1").last_name
    params = {"username":"student_coll1_1",
              "password":"cows",
              "new_last_name":"",
              }

    r, data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200
    assert User("student_coll1_1").last_name == old_last

def test_student_post_doesnt_set_first_last_name():
    old_first = "student1i"
    old_last  = "student"

    params = {"username":"student_coll1_1",
              "password":"cows",
              "new_first_name":"asdf",
              "new_last_name":"cheese",
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200

    details_dict = User("student_coll1_1").details_dictionary_for(User.create_user("student_coll1_1", "cows"))

    # restore original data
    u = User("student_coll1_1")
    u.set_first_name(old_first)
    u.set_last_name(old_last)
    u.save()

    assert details_dict["first_name"] == old_first
    assert details_dict["last_name"] == old_last

def test_student_cant_set_team_leader():
    params = {"username": "student_coll1_1",
              "password": "cows",
              "new_type": "team-leader",
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200

    assert not User("student_coll1_1").is_teacher

def test_team_leader_can_set_team_leader():
    params = {"username": "teacher_coll1",
              "password": "facebees",
              "new_type": "team-leader",
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200

    u = User("student_coll1_1")
    is_teacher = u.is_teacher

    # Clean up
    u.make_student()
    u.save()

    # now assert (ensures the clean-up occurs)
    assert is_teacher

def test_team_leader_can_become_student():
    # We need to test against another teacher, because team leaders demoting themselves is not allowed
    u = User("student_coll1_1")
    u.make_teacher()
    u.save()

    params = {"username": "teacher_coll1",
              "password": "facebees",
              "new_type": "student",
              }

    r,data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200

    assert not User("student_coll1_1").is_teacher

def test_team_leader_cant_demote_self():
    params = {"username": "teacher_coll1",
              "password": "facebees",
              "new_type": "student",
              }

    r,data = test_helpers.server_post("/user/teacher_coll1", params)
    assert r.status == 200

    assert User("teacher_coll1").is_teacher

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

def unwithdraw(username):
    def do_unwithdrawal():
        group = srusers.group('withdrawn')
        group.user_rm(username)
        group.save()
    return do_unwithdrawal

@with_setup(None, unwithdraw('student_coll1_1'))
def test_post_teacher_can_withdraw_student():
    params = {"username":"teacher_coll1",
              "password":"facebees",
              "withdrawn":'true',
              }

    r, data = test_helpers.server_post("/user/student_coll1_1", params)
    assert r.status == 200

    assert User("student_coll1_1").has_withdrawn

def test_post_student_cant_withdraw_other_student():
    params = {"username":"student_coll1_1",
              "password":"cows",
              "withdrawn":'true',
              }

    r, data = test_helpers.server_post("/user/student_coll1_2", params)
    assert r.status == 403

    assert not User("student_coll1_2").has_withdrawn

def test_post_teacher_cant_withdraw_self():
    params = {"username":"teacher_coll1",
              "password":"facebees",
              "withdrawn":'true',
              }

    r, data = test_helpers.server_post("/user/teacher_coll1", params)
    assert r.status == 200

    assert not User("teacher_coll1").has_withdrawn
