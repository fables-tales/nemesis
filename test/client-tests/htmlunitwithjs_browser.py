
import os
from selenium import webdriver

browser = None

# Default for developing, modify if needed
root_url = 'http://localhost:5000'

def get_browser():
    global browser

    # Requires that the selenium jar is running
    browser = webdriver.Remote(desired_capabilities = webdriver.DesiredCapabilities.HTMLUNITWITHJS)
    return browser

def end_browser():
    browser.quit()
