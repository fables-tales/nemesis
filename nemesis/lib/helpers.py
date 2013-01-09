import sqlite3
import os
import json

PATH = os.path.dirname(os.path.abspath(__file__)) + "/../"

def deauth_debug_response(total_deleted_tokens):
    if total_deleted_tokens == 1:
        deleted = True
    else:
        deleted = False

    return json.dumps({"deleted": str(deleted)}), 200

def sqlite_connect():
    return sqlite3.connect(PATH + "/db/nemesis.sqlite")

def register_user(teacher_username, college_group, first_name, last_name, email, team):
    conn = sqlite_connect()
    cur = conn.cursor()
    prep_statement = "INSERT INTO registrations (teacher_username, college_group, first_name, last_name, email, team) VALUES (?,?,?,?,?,?)";
    cur.execute(prep_statement, (teacher_username, college_group, first_name, last_name, email, team))
    conn.commit()




