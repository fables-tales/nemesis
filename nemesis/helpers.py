import sqlite3
import os

PATH = os.path.dirname(os.path.abspath(__file__))

def sqlite_connect():
    return sqlite3.connect(PATH + "/db/nemesis.sqlite")

def register_user(teacher_username, college_group, first_name, last_name, email, team):
    conn = sqlite_connect()
    cur = conn.cursor()
    prep_statement = "INSERT INTO registrations (teacher_username, college_group, first_name, last_name, email, team) VALUES (?,?,?,?,?, ?)";
    cur.execute(prep_statement, (teacher_username, college_group, first_name, last_name, email))
    conn.commit()




