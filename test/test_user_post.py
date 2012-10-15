import unittest
import json
import helpers

class TestAuth(unittest.TestCase):

    def setUp(self):
        resp_auth = helpers.server_post("/auth", {"username":"teacher_coll1", "password":"facebees"})
        self.auth_hash = json.loads(resp_auth.read())["token"]

    def tearDown(self):
        deauth = helpers.server_post("/deauth", {"token":self.auth_hash})

if __name__ == '__main__':
    unittest.main()
