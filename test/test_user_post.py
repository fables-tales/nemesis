import unittest
import json
import helpers
import random
from serverldap import LdapInstance

class TestAuth(unittest.TestCase):

    def setUp(self):
        resp_auth = helpers.server_post("/auth", {"username":"teacher_coll2", "password":"noway"})
        self.auth_hash = json.loads(resp_auth.read())["token"]

    def tearDown(self):
        deauth = helpers.server_post("/deauth", {"token":self.auth_hash})


    def test_user_post_set_nothing_code(self):
        resp = helpers.server_post("/user/student_coll2_1", {"token":self.auth_hash})
        self.assertEqual(resp.status, 200)

    def test_user_post_set_email_code(self):
        args_hash = {}
        args_hash["token"] = self.auth_hash
        args_hash["email"] = "sam@sam.com"
        resp = helpers.server_post("/user/student_coll2_1", args_hash)
        self.assertEqual(resp.status, 200)

    def test_user_post_set_email_email(self):
        args_hash = {}
        args_hash["token"] = self.auth_hash
        args_hash["email"] = "sam@sam" + str(random.randint(0,10000)) + ".com"
        resp = helpers.server_post("/user/student_coll2_2", args_hash)
        self.assertEqual(resp.status, 200)

        resp = helpers.server_get("/user/student_coll2_2", {"token":self.auth_hash})
        body = json.loads(resp.read())
        self.assertEqual(body["email"], args_hash["email"])

    def test_user_post_set_password_code(self):
        args_hash = {}
        args_hash["token"] = self.auth_hash
        args_hash["password"] = "abc" + str(random.randint(0,10000))
        resp = helpers.server_post("/user/student_coll2_2", args_hash)
        self.assertEqual(resp.status, 200)

    def test_user_post_set_password_password(self):
        args_hash = {}
        args_hash["token"] = self.auth_hash
        args_hash["password"] = "abc" + str(random.randint(0,10000))
        resp = helpers.server_post("/user/student_coll2_2", args_hash)
        instance = LdapInstance("../nemesis/userman")
        bind_result = instance.bind("student_coll2_2", args_hash["password"])
        self.assertTrue(bind_result)

if __name__ == '__main__':
    unittest.main()
