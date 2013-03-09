import test_helpers

def test_registration_no_user():
    r,data = test_helpers.server_post("/registrations")
    assert r.status == 403

def test_registration_user_and_form():
    test_helpers.delete_db()
    params = {"username":"teacher_coll1",
              "password":"facebees",
              "first_name":"register",
              "last_name":"this.user",
              "email":"bob@example.com",
              "team":"team-ABC",
              "college":"college-1"}

    r,data = test_helpers.server_post("/registrations", params)
    assert r.status == 200
    assert len(test_helpers.get_registrations()) == 1
    test_helpers.delete_db()

def test_registration_wrong_college():
    test_helpers.delete_db()

    params = {"username":"teacher_coll1",
              "password":"facebees",
              "first_name":"register",
              "last_name":"this.user",
              "email":"bob@example.com",
              "team":"team-ABC",
              "college":"college-2"}

    r,data = test_helpers.server_post("/registrations", params)
    assert r.status == 403
    assert len(test_helpers.get_registrations()) == 0
    test_helpers.delete_db()
