import unittest
from hashlib import sha256
import random
import json
import test_helpers as helpers

class TestDeauth(unittest.TestCase):
    def setUp(self):
        pass

    def test_deauth_no_token_code(self):
        resp = helpers.server_post("/deauth", {})
        self.assertEqual(resp.status, 200)

    def test_deauth_no_token_body(self):
        resp = helpers.server_post("/deauth", {})
        if helpers.apache_mode():
            self.assertEqual(resp.read(), '')
        else:
            self.assertEqual(resp.read(), "False")

    def test_deauth_invalid_token_code(self):
        auth_hash = {"token":sha256(str(random.randint(0,1000000))).hexdigest()}
        resp = helpers.server_post("/deauth", auth_hash)
        self.assertEqual(resp.status, 200)

    def test_deauth_invalid_token_body(self):
        auth_hash = {"token":sha256(str(random.randint(0,1000000))).hexdigest()}
        resp = helpers.server_post("/deauth", auth_hash)
        if helpers.apache_mode():
            self.assertEqual(resp.read(), '')
        else:
            self.assertEqual(resp.read(), "False")

    def test_deauth_valid_token_code(self):
        resp_auth = helpers.server_post("/auth", {"username":"teacher_coll1", "password":"facebees"})
        auth_hash = json.loads(resp_auth.read())
        resp = helpers.server_post("/deauth", auth_hash)
        self.assertEqual(resp.status, 200)

    def test_deauth_valid_token_body(self):
        resp_auth = helpers.server_post("/auth", {"username":"teacher_coll1", "password":"facebees"})
        value = resp_auth.read()
        auth_hash = json.loads(value)
        resp = helpers.server_post("/deauth", auth_hash)
        if helpers.apache_mode():
            self.assertEqual(resp.read(), '')
        else:
            self.assertEqual(resp.read(), "True")

if __name__ == '__main__':
    unittest.main()
