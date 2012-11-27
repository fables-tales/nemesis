import unittest
import json
import test_helpers as helpers

class TestCollege(unittest.TestCase):

    def setUp(self):
        resp_auth = helpers.server_post("/auth", {"username":"teacher_coll1", "password":"facebees"})
        self.auth_hash = json.loads(resp_auth.read())["token"]

    def tearDown(self):
        deauth = helpers.server_post("/deauth", {"token":self.auth_hash})

    def test_get_college_code(self):
        resp = helpers.server_get("/college", {"token":self.auth_hash})
        self.assertEqual(resp.status, 200)

    def test_get_college_body(self):
        resp = helpers.server_get("/college", {"token":self.auth_hash})
        obj = json.loads(resp.read())
        self.assertTrue(obj.has_key("userids"))
        self.assertTrue("teacher_coll1" in obj["userids"])
        self.assertTrue("student_coll1_1" in obj["userids"])
        self.assertTrue("student_coll1_2" in obj["userids"])

        self.assertEqual(obj["college_name"], "college the first")
        self.assertTrue("team-ABC" in obj["teams"])
        self.assertTrue("team-DFE" in obj["teams"])

    def test_get_college_noauth(self):
        resp = helpers.server_get("/college")
        self.assertEqual(resp.status, 403)

if __name__ == '__main__':
    unittest.main()
