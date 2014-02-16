
from selenium.common.exceptions import StaleElementReferenceException
import time
import unittest

import test_helpers as helpers
from test_helpers import wait_while

class testUserman(unittest.TestCase):
    def tearDown(self):
        helpers.end_browser()
        helpers.remove_user('1_ww1')
        helpers.clear_database()

    def setUp(self):
        helpers.remove_user('1_ww1')
        helpers.clear_database()
        b = helpers.get_browser()
        self.browser = b

    def login(self, user = 'teacher_coll1', passwd = 'facebees'):
        self.assert_shown('login')

        username = self.assert_shown('username')
        username.send_keys(user)

        password = self.assert_shown('password')
        password.send_keys(passwd)

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
        not_shown = lambda: not self.browser.find_element_by_css_selector(elem_selector).is_displayed()
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

    def get_messages_text(self):
        return self.assert_shown('messages').text


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
                    'withdrawn_student']:
            self.assert_shown_selector('#college-1 li.{0}'.format(uid))

    def test_register(self):
        self.login()

        # Get the registration form showing
        reg_link = self.assert_shown_selector('#college-1 li.register a')
        reg_link.click()

        current_url = self.browser.current_url
        assert "#reg-college-1" in current_url

        time.sleep(0.5)

        reg_li = self.assert_shown_selector('#college-1 li.register')
        reg_li_classes = reg_li.get_attribute('class')
        assert 'active' in reg_li_classes

        self.assert_shown("data-register-users")
        self.assert_shown("data-register-table")
        first_name_1 = self.assert_shown_selector("#data-register-table input[name=first_name]")
        assert first_name_1.is_selected, 'focus should be on the first_name input'

        # Actually submit a new user
        last_name_1 = self.assert_shown_selector("#data-register-table input[name=last_name]")
        email_1 = self.assert_shown_selector("#data-register-table input[name=email]")
        feedback_1 = self.assert_shown_selector("#data-register-table td.feedback")

        first_name_1.send_keys("winning")
        last_name_1.send_keys("winning")
        email_1.send_keys("winning@example.com")

        register_button = self.assert_shown("register-submit")
        register_button.click()
        feedback = feedback_1.text
        assert feedback == '', feedback

        msg_text = self.get_messages_text()
        assert '0/1' in msg_text

        time.sleep(1)

        try:
            feedback = feedback_1.text
            assert feedback == '', feedback
        except StaleElementReferenceException:
            pass # it gets removed on success

        msg_text = self.get_messages_text()
        assert 'success' in msg_text, msg_text

        register_users_div = self.browser.find_element_by_id("data-register-users")
        assert not register_users_div.is_displayed()

        self.assertEqual(helpers.registration_count(), 1)

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

    def test_self_edit_link_student(self):
        self.login('student_coll1_1', 'cows')

        self_link = self.assert_shown_selector('#logged-in-user a')
        assert "student1 student (student_coll1_1)" == self_link.text

        self_link.click()
        self.assert_editing('student_coll1_1')

    def test_change_user_details(self):
        self.test_user_display()

        email_field = self.assert_shown_selector("#update-user input[name=new_email]")
        email_field.clear()
        new_email = "email2@example.com"
        email_field.send_keys(new_email)

        set_button = self.assert_shown("edit-submit")
        set_button.click()

        msg_text = self.get_messages_text()
        assert 'sending user detail' in msg_text.lower(), msg_text

        time.sleep(1)

        # Should still be showing the same user
        self.assert_editing('student_coll1_1')

        # Should have the new email as a pending
        email_field = self.assert_shown("data-email")
        email_field_text = email_field.text
        expected = "pending change to " + new_email
        assert expected in email_field_text, email_field_text

if __name__ == '__main__':
    unittest.main()
