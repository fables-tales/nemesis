import unittest
import helpers

class TestAuth(unittest.TestCase):

    def setUp(self):
        pass

    def test_auth_invalid_resp_code(self):
        resp = helpers.server_post("/auth", {"username":"wrong", "password":"fail"})
        self.assertEqual(resp.status, 403)

    def test_auth_invalid_body(self):
        resp = helpers.server_post("/auth", {"username":"wrong", "password":"fail"})
        self.assertEqual(resp.read(), "")

    def test_auth_valid_resp_code(self):
        resp = helpers.server_post("/auth", {"username":"teacher_coll1", "password":"facebees"})
        self.assertEqual(resp.status, 200)

    def test_auth_valid_body(self):
        resp = helpers.server_post("/auth", {"username":"teacher_coll1", "password":"facebees"})
        resp = resp.read()
        self.assertTrue(resp.find("{\"auth\":") != -1)
        self.assertTrue(resp.find("}") != -1)

    def test_auth_valid_not_teacher_code(self):
        self.fail()


#    def test_shuffle(self):
#        # make sure the shuffled sequence does not lose any elements
#        random.shuffle(self.seq)
#        self.seq.sort()
#        self.assertEqual(self.seq, range(10))
#
#        # should raise an exception for an immutable sequence
#        self.assertRaises(TypeError, random.shuffle, (1,2,3))
#
#    def test_choice(self):
#        element = random.choice(self.seq)
#        self.assertTrue(element in self.seq)
#
#    def test_sample(self):
#        with self.assertRaises(ValueError):
#            random.sample(self.seq, 20)
#        for element in random.sample(self.seq, 5):
#            self.assertTrue(element in self.seq)
#
if __name__ == '__main__':
    unittest.main()
