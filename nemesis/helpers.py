
import datetime
import hashlib
import random
import sqlite3
import os

PATH = os.path.dirname(os.path.abspath(__file__))

def sqlite_connect():
    return sqlite3.connect(PATH + "/db/nemesis.sqlite")

def _exec(statement, arguments):
    conn = sqlite_connect()
    cur = conn.cursor()
    cur.execute(statement, arguments)
    conn.commit()

def is_email_request_valid(request):
    rq_age = datetime.datetime.now() - request['request_time']
    is_young_enuogh = rq_age < datetime.timedelta(days = 2)
    return is_young_enuogh

def get_change_email_request(username):

    prep_statement = "SELECT username, new_email, request_time, verify_code FROM email_changes WHERE username=?"

    conn = sqlite_connect()
    cur = conn.cursor()
    cur.execute(prep_statement, (username,))
    row = cur.fetchone()
    if row is None:
        return None

    rq_time = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
    request = { 'username': row[0]
               ,'new_email': row[1]
               ,'request_time': rq_time
               ,'verify_code': row[3]
              }
    return request

def new_email(username, new_email, verify_code):
    if get_change_email_request(username = username) is not None:
        prep_statement = "UPDATE email_changes SET new_email=?, verify_code=?, request_time=CURRENT_TIMESTAMP WHERE username=?"
        _exec(prep_statement, (new_email, verify_code, username))
    else:
        prep_statement = "INSERT INTO email_changes (username, new_email, verify_code) VALUES (?,?,?)"
        _exec(prep_statement, (username, new_email, verify_code))

def clear_new_email_request(username):
    if get_change_email_request(username = username) is not None:
        prep_statement = "DELETE FROM email_changes WHERE username=?"
        _exec(prep_statement, (username, ))

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
