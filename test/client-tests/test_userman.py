
import time
import unittest

import test_helpers as helpers

def wait_while(predicate, max = 5):
    end = time.time() + max
    while predicate():
        time.sleep(0.1)
        if time.time() > end:
            break

class testUserman(unittest.TestCase):
    def tearDown(self):
        helpers.end_browser()

    def reset_user_details(self):
        helpers.end_browser()
        self.browser = helpers.get_browser()
        self.login()
        user_link = self.browser.find_element_by_id("user-student_coll1_1")
        user_link.click()
        print "user details sleep"
        time.sleep(4)
        print "user details sleep done"

        email_field = self.browser.find_element_by_id("user-email")
        email_field.clear()
        email_field.send_keys("student1@example.com")

        password_field = self.browser.find_element_by_id("user-password")
        password_field.clear()
        password_field.send_keys("cows")

        set_button = self.browser.find_element_by_id("set")
        set_button.click()
        time.sleep(4)

    def setUp(self):
        helpers.clear_database()
        b = helpers.get_browser()
        self.browser = b

    def login(self):
        self.assert_shown('login')

        username = self.assert_shown('username')
        username.send_keys("teacher_coll1")

        password = self.assert_shown('password')
        password.send_keys("facebees")

        login_button = self.browser.find_element_by_css_selector('#login button')
        login_button.click()
        messages = self.assert_shown('messages')
        curr_msg = messages.text
        assert curr_msg == 'Logging in...'
        time.sleep(2.5)

    def assert_shown(self, elem_id):
        elem = self.browser.find_element_by_id(elem_id)
        assert elem.is_displayed(), "{0} should be shown".format(elem_id)
        return elem

    def assert_shown_selector(self, elem_selector):
        elem = self.browser.find_element_by_css_selector(elem_selector)
        assert elem.is_displayed(), "{0} should be shown".format(elem_id)
        return elem

    def assert_not_shown(self, elem_id):
        elem = self.browser.find_element_by_id(elem_id)
        assert not elem.is_displayed(), "{0} should not be shown".format(elem_id)
        return elem

    def wait_shown(self, elem_id, max = 5):
        not_shown = lambda: not self.browser.find_element_by_id(elem_id).is_displayed()
        wait_while(not_shown, max)
        return self.assert_shown(elem_id)

    def wait_shown_selector(self, elem_selector, max = 5):
        not_shown = lambda: not self.browser.find_element_by_css_selector(elem_id).is_displayed()
        wait_while(not_shown, max)
        return self.assert_shown_selector(elem_selector)


    def assert_editing(self, username):
        anchor = '#edit-' + username
        url = self.browser.current_url
        assert anchor in url

        user_li = self.assert_shown_selector('#college-1 li.user.' + username)
        classes = user_li.get_attribute('class')
        assert 'active' in classes

        self.wait_shown('data-edit-user', 1)
        header = self.assert_shown_selector('#data-edit-user h2')
        assert username in header.text


    def test_landingpage_title(self):
        assert self.browser.title == "Userman"
        self.assert_shown('login')
        self.assert_shown('username')
        self.assert_shown('password')

    def test_landingpage_login(self):
        self.login()
        self.assert_shown('data-college-list')
        college_1 = self.assert_shown('college-1')
        college_1_text = college_1.text
        assert "college the first" in college_1_text.lower(), college_1_text
        self.assert_shown_selector('#college-1 li.register')
        for uid in ['teacher_coll1', 'student_coll1_1', 'student_coll1_2', \
                    'blueshirt', 'withdrawn_student']:
            self.assert_shown_selector('#college-1 li.{0}'.format(uid))

    def test_landingpage_register(self):
        self.login()

        reg_link = self.assert_shown_selector('#college-1 li.register a')
        reg_link.click()

        current_url = self.browser.current_url
        assert "#reg-college-1" in current_url

        time.sleep(0.5)

        reg_li = self.assert_shown_selector('#college-1 li.register')
        reg_li_classes = reg_li.get_attribute('class')
        assert 'active' in reg_li_classes

        register_users_div = self.assert_shown("data-register-users")
        register_users_table = self.assert_shown("data-register-table")
        first_name_1 = self.assert_shown_selector("#data-register-table input[name=first_name]")
        assert first_name_1.is_selected, 'focus should be on the first_name input'

    def test_user_display(self):
        self.login()

        user_li = self.assert_shown_selector('#college-1 li.user.student_coll1_1')
        classes = user_li.get_attribute('class')
        assert 'active' not in classes

        user_link = self.assert_shown_selector('#college-1 li.user.student_coll1_1 a')
        assert "student1 student (student_coll1_1)" == user_link.text

        user_link.click()
        self.assert_editing('student_coll1_1')

    def test_self_edit_link(self):
        self.login()

        self_link = self.assert_shown_selector('#logged-in-user a')
        assert "teacher teacher (teacher_coll1)" == self_link.text

        self_link.click()
        self.assert_editing('teacher_coll1')

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
        time.sleep(7)

        msg_div = self.browser.find_element_by_id("msg")
        print self.browser.current_url

        self.assertTrue("#college" in self.browser.current_url)
        self.assertEqual(msg_div.text, "1 users registered successfully!")
        self.assertEqual(helpers.registration_count(), 1)


    def test_change_user_details(self):
        self.login()
        print "."
        user_link = self.browser.find_element_by_id("user-student_coll1_1")
        user_link.click()
        print "."
        time.sleep(1)
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
        time.sleep(2)
        print "."
        email_field = self.browser.find_element_by_id("user-email")
        self.assertEqual(email_field.get_attribute("value"), "email2@email.com")

        print "."
        print "starting reset"
        self.reset_user_details()
        print "reset done"

if __name__ == '__main__':
    unittest.main()
