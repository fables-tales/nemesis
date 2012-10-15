import unittest
import helpers
from serverldap import LdapInstance

class TestAuth(unittest.TestCase):

    def setUp(self):
        pass

    def test_is_teacher_teacher(self):
        self.assertTrue(LdapInstance("../nemesis/userman").is_teacher("teacher_coll1"))

if __name__ == '__main__':
    unittest.main()
