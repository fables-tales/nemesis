from pyvirtualdisplay import Display
from selenium import webdriver

display = Display(visible=0, size=(800, 600))
display.start()

browser = webdriver.Firefox()

def get_browser():
    return browser
