import unittest
from serverldap import LdapInstance, is_teacher_of

class TestLdap(unittest.TestCase):

    def setUp(self):
        pass

    def test_is_teacher_teacher(self):
        self.assertTrue(LdapInstance("../../nemesis/userman").is_teacher("teacher_coll1"))

    def test_is_teacher_of_teacher(self):
        self.assertTrue(is_teacher_of("../../nemesis/userman", "teacher_coll1", "student_coll1_1"))

    def test_manager_bind(self):
        self.assertTrue(LdapInstance("../../nemesis/userman").manager_bind())

    def test_set_user_email(self):
        instance = LdapInstance("../../nemesis/userman")
        instance.set_user_attribute("teacher_coll2", "mail", "mail@mail.com")
        self.assertTrue(instance.get_user_details("teacher_coll2")["E-mail"], "mail@mail.com")

    def test_get_college_name(self):
        instance = LdapInstance("../../nemesis/userman")
        group = instance.get_college("teacher_coll1")
        print group
        self.assertEqual(group.name(), "college the first")
        group = instance.get_college("teacher_coll2")
        self.assertEqual(group.name(), "secondary college")

    def test_get_college_teams_1(self):
        instance = LdapInstance("../../nemesis/userman")
        teams = instance.get_college("teacher_coll1").teams()
        print teams
        self.assertTrue("team-ABC" in teams)
        self.assertTrue("team-DFE" in teams)
        self.assertEqual(len(teams), 2)

    def test_get_college_teams_2(self):
        instance = LdapInstance("../../nemesis/userman")
        teams = instance.get_college("teacher_coll2").teams()
        self.assertTrue("team-QWZ" in teams)
        self.assertEqual(len(teams), 1)

if __name__ == '__main__':
    unittest.main()
