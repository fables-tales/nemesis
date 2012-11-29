from pyvirtualdisplay import Display
from selenium import webdriver
import sqlite3


browser = None
display = None

def get_browser():
    global browser
    global display
    display = Display(visible=0, size=(800, 600))
    display.start()

    browser = webdriver.Firefox(timeout=10)
    browser.get("https://localhost/userman")
    return browser

def end_browser():
    browser.quit()
    display.stop()

def sqlite_connect():
    conn = sqlite3.connect("../../nemesis/db/nemesis.sqlite")
    return conn

def clear_database():
    conn = sqlite_connect()
    cur  = conn.cursor()
    cur.execute("DELETE FROM registrations")
    conn.commit()

def registration_count():
    conn = sqlite_connect()
    cur  = conn.cursor()
    return cur.execute("SELECT COUNT(*) FROM registrations").next()[0]
