import unittest
import test_helpers as helpers
import time


class testUserman(unittest.TestCase):
    def tearDown(self):
        helpers.end_browser()

    def reset_user_details(self):
        helpers.end_browser()
        self.browser = helpers.get_browser()
        time.sleep(1)
        self.login()
        user_link = self.browser.find_element_by_id("user-student_coll1_1")
        user_link.click()
        print "user details sleep"
        time.sleep(3)
        print "user details sleep done"

        email_field = self.browser.find_element_by_id("user-email")
        email_field.clear()
        email_field.send_keys("student1@teacher.com")

        password_field = self.browser.find_element_by_id("user-password")
        password_field.clear()
        password_field.send_keys("cows")

        set_button = self.browser.find_element_by_id("set")
        set_button.click()
        time.sleep(2)

    def setUp(self):
        helpers.clear_database()
        b = helpers.get_browser()
        self.browser = b

    def login(self):
        time.sleep(1.5)
        username = self.browser.find_element_by_id("username")
        username.send_keys("teacher_coll1")

        password = self.browser.find_element_by_id("password")
        password.send_keys("facebees")

        login_button = self.browser.find_element_by_id("go")
        login_button.click()
        time.sleep(4)

    def test_landingpage_title(self):
        self.assertEqual(self.browser.title,"Student Robotics Userman")
        college = self.browser.find_element_by_id("college")
        self.assertFalse(college.is_displayed())

    def test_landingpage_login(self):
        self.login()

        college = self.browser.find_element_by_id("college")
        self.assertTrue(college.is_displayed())

    def test_landingpage_register(self):
        self.login()

        registration_link = self.browser.find_element_by_id("show-register")
        registration_link.click()
        register_users_div = self.browser.find_element_by_id("register-users")

        self.assertTrue("#register-users" in self.browser.current_url)
        self.assertTrue(register_users_div.is_displayed())

    def test_landingpage_user(self):
        self.login()
        user_link = self.browser.find_element_by_link_text("student1 student")
        user_link.click()
        user_div = self.browser.find_element_by_id("user")
        time.sleep(3)
        self.assertTrue("#show-student_coll1_1" in self.browser.current_url)
        self.assertTrue(user_div.is_displayed())

    def test_register(self):
        self.login()
        registration_link = self.browser.find_element_by_id("show-register")
        registration_link.click()
        time.sleep(1)
        form = self.browser.find_elements_by_xpath('//*/td/input')
        form[0].send_keys("winning")
        form[1].send_keys("winning")
        form[2].send_keys("winning")

        register_button = self.browser.find_element_by_id("send-register")
        register_button.click()
        time.sleep(4)

        msg_div = self.browser.find_element_by_id("msg")

        self.assertTrue("#college" in self.browser.current_url)
        self.assertEqual(msg_div.text, "1 users registered successfully!")
        self.assertEqual(helpers.registration_count(), 1)


    def test_change_user_details(self):
        self.login()
        print "."
        user_link = self.browser.find_element_by_id("user-student_coll1_1")
        user_link.click()
        print "."
        time.sleep(3)
        print "."
        self.assertTrue("#show-student_coll1_1" in self.browser.current_url)

        password_field = self.browser.find_element_by_id("user-password")
        password_field.clear()
        password_field.send_keys("my_new_password")

        email_field = self.browser.find_element_by_id("user-email")
        email_field.clear()
        email_field.send_keys("email2@email.com")

        set_button = self.browser.find_element_by_id("set")
        set_button.click()
        print "."
        time.sleep(2)
        print "."
        user_link = self.browser.find_element_by_id("user-student_coll1_1")
        user_link.click()
        print "."
        time.sleep(4)
        print "."
        email_field = self.browser.find_element_by_id("user-email")
        self.assertEqual(email_field.get_attribute("value"), "email2@email.com")

        print "."
        print "starting reset"
        self.reset_user_details()
        print "reset done"

if __name__ == '__main__':
    unittest.main()
