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

def register_user(teacher_username, college_group, first_name, last_name, email, team):
    prep_statement = "INSERT INTO registrations (teacher_username, college_group, first_name, last_name, email, team) VALUES (?,?,?,?,?,?)";
    _exec(prep_statement, (teacher_username, college_group, first_name, last_name, email, team))
