import unittest
import test_helpers as helpers

class TestRev(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_rev_code(self):
        resp = helpers.server_get("/site/sha")
        self.assertEqual(resp.status, 200)

    def test_get_rev_code_body(self):
        resp = helpers.server_get("/site/sha")
        self.assertTrue(len(resp.read()) > 16)

if __name__ == '__main__':
    unittest.main()
