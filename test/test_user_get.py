import unittest
import json
import helpers

class TestAuth(unittest.TestCase):

    def setUp(self):
        resp_auth = helpers.server_post("/auth", {"username":"teacher_coll1", "password":"facebees"})
        self.auth_hash = json.loads(resp_auth.read())["token"]

    def tearDown(self):
        deauth = helpers.server_post("/deauth", {"token":self.auth_hash})

    def test_user_get_valid_teacher_code(self):
        resp = helpers.server_get("/user/student_coll1_1", {"token":self.auth_hash})
        self.assertEqual(resp.status, 200)

    def test_user_get_valid_teacher_body(self):
        resp = helpers.server_get("/user/student_coll1_1", {"token":self.auth_hash})
        body = resp.read()
        hash = json.loads(body)
        self.assertEqual(hash["full_name"], "student1 student")
        self.assertEqual(hash["email"], "student1@teacher.com")


    def test_user_get_valid_teacher_no_user(self):
        resp = helpers.server_get("/user/wqoifjwqfie", {"token":self.auth_hash})
        self.assertNotEqual(resp.status, 200)

if __name__ == '__main__':
    unittest.main()
