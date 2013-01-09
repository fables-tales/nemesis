import unittest
import test_helpers as helpers
from lib.serverldap import User

class TestLdap(unittest.TestCase):

    def setUp(self):
        pass

    def test_is_teacher_teacher(self):
        self.assertTrue(User("teacher_coll1", "../../nemesis/userman").is_teacher())

    def test_is_teacher_of_teacher(self):
        self.assertTrue(User("teacher_coll1", "../../nemesis/userman").is_teacher_of("student_coll1_1"))

    def test_manager_bind(self):
        self.assertTrue(User("","../../nemesis/userman").conn.manager_bind())

    def test_set_user_email(self):
        instance = User("teacher_coll2","../../nemesis/userman")
        instance.conn.set_user_attribute("teacher_coll2", "mail", "mail@mail.com")
        self.assertTrue(instance.user_details()["E-mail"], "mail@mail.com")

    def test_get_college_name(self):
        instance = User("teacher_coll1", "../../nemesis/userman")
        group = instance.college()
        self.assertEqual(group.name(), "college the first")

        instance = User("teacher_coll2", "../../nemesis/userman")
        group = instance.college()
        self.assertEqual(group.name(), "secondary college")

    def test_get_college_teams_1(self):
        instance = User("teacher_coll1", "../../nemesis/userman")
        teams = instance.college().teams()
        print teams
        self.assertTrue("team-ABC" in teams)
        self.assertTrue("team-DFE" in teams)
        self.assertEqual(len(teams), 2)

    def test_get_college_teams_2(self):
        instance = User("teacher_coll2", "../../nemesis/userman")
        teams = instance.college().teams()
        self.assertTrue("team-QWZ" in teams)
        self.assertEqual(len(teams), 1)

if __name__ == '__main__':
    unittest.main()
