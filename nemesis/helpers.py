
import datetime
import hashlib
import random
import sqlite3
import os

PATH = os.path.dirname(os.path.abspath(__file__))

def sqlite_connect():
    return sqlite3.connect(PATH + "/db/nemesis.sqlite")

def create_verify_code(username, new_email):
    """
    An increadibly weak way of generating a 'random' looking string which
    we can use to verify the authenticity of an email address.
    The aim here is mostly to check that it exists, so absolute security
    isn't strictly needed. The overall length is 160 characters.
    """
    user_part = hashlib.md5(username + new_email).hexdigest()
    random_part = hex(random.getrandbits(128))[2:-1]
    code = random_part + user_part
    return code
