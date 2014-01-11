
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import test_helpers

browser = None

# Default for developing, modify if needed
root_url = 'http://localhost:5000'

def get_browser():
    global browser

    my_dir = os.path.dirname(os.path.abspath(__file__))

    # Un comment the line below to use chromedriver directly, and
    # modify with the path to your chromedriver download if needed
    #browser = webdriver.Chrome(os.path.join(my_dir, 'chromedriver'))

    # Use Chrome via the server, expects chromedriver to be next to the jar.
    browser = webdriver.Remote(desired_capabilities = DesiredCapabilities.CHROME)

    return browser

def end_browser():
    browser.quit()
