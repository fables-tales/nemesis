import unittest
import helpers
from serverldap import LdapInstance, is_teacher_of

class TestAuth(unittest.TestCase):

    def setUp(self):
        pass

    def test_is_teacher_teacher(self):
        self.assertTrue(LdapInstance("../nemesis/userman").is_teacher("teacher_coll1"))

    def test_is_teacher_of_teacher(self):
        self.assertTrue(is_teacher_of("../nemesis/userman", "teacher_coll1", "student_coll1_1"))

if __name__ == '__main__':
    unittest.main()
