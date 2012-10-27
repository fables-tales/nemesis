import unittest
import test_helpers as helpers

class TestAuth(unittest.TestCase):

    def setUp(self):
        pass

    def test_auth_invalid_resp_code(self):
        resp = helpers.server_post("/auth", {"username":"wrong", "password":"fail"})
        self.assertEqual(resp.status, 403)

    def test_auth_invalid_body(self):
        resp = helpers.server_post("/auth", {"username":"wrong", "password":"fail"})
        self.assertEqual(resp.read(), '{"error": "invalid credentials"}')

    def test_auth_valid_resp_code(self):
        resp = helpers.server_post("/auth", {"username":"teacher_coll1", "password":"facebees"})
        self.assertEqual(resp.status, 200)

        resp = helpers.server_post("/auth", {"username":"teacher_coll2", "password":"noway"})
        self.assertEqual(resp.status, 200)

    def test_auth_valid_body(self):
        resp = helpers.server_post("/auth", {"username":"teacher_coll1", "password":"facebees"})
        resp = resp.read()
        self.assertTrue(resp.find("{\"token\":") != -1)
        self.assertTrue(resp.find("}") != -1)

    def test_auth_valid_not_teacher_code(self):
        #tests that we can't login as a student, even with a valid username
        #and password
        resp = helpers.server_post("/auth", {"username":"student_coll1_1", "password":"cows"})
        self.assertEqual(resp.status, 403)

    def test_auth_valid_not_teacher_body(self):
        resp = helpers.server_post("/auth", {"username":"student_coll1_1", "password":"cows"})
        self.assertEqual(resp.read(), '{"error": "not a teacher"}')

if __name__ == '__main__':
    unittest.main()
