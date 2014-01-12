
from pyvirtualdisplay import Display
from selenium import webdriver

browser = None
display = None

root_url = 'https://localhost/userman'

def get_browser():
    global browser
    global display
    display = Display(visible=0, size=(800, 600))
    display.start()

    browser = webdriver.Firefox(timeout=10)
    return browser

def end_browser():
    browser.quit()
    display.stop()
