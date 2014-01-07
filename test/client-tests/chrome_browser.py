
import os
from selenium import webdriver

import test_helpers

browser = None

# Default for developing, modify if needed
root_url = 'http://localhost:5000'

def get_browser():
    global browser

    my_dir = os.path.dirname(os.path.abspath(__file__))

    # modify with the path to your chromedriver download if needed
    browser = webdriver.Chrome(os.path.join(my_dir, 'chromedriver'))
    return browser

def end_browser():
    browser.quit()
