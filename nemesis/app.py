import os
import subprocess
import json

from lib.serverldap import User, handle_authentication, get_username
from lib.helpers import sqlite_connect
from flask import Flask, request

import lib.helpers as helpers

PATH = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

@app.route("/")
def index():
    return open(PATH + '/templates/index.html').read()

@app.route("/site/sha")
def sha():
    p = subprocess.Popen(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE, cwd=PATH)
    p.wait()
    return p.stdout.read()

@app.route("/auth", methods=["POST"])
def auth():
    if request.form.has_key("username") and request.form.has_key("password"):
        username = request.form["username"]
        password = request.form["password"]
        user = User(username, PATH + "/userman")
        if user.password_is_valid(password):
            return user.authentication_response()
        else:
            return '{"error": "invalid credentials"}', 403
    return '', 403


@app.route("/deauth", methods=["POST"])
def deauth():
    count = 0
    if request.form.has_key("token"):
        token = request.form["token"]
        c = sqlite_connect()
        cur = c.cursor()
        cur.execute("DELETE FROM auth WHERE token=?", (token,))
        c.commit()
        count = c.total_changes

    if app.debug:
        return helpers.deauth_debug_response(count)
    else:
        return '',200

@app.route("/user/register", methods=["POST"])
def register_user():
    if handle_authentication(request.form):
        teacher_username = get_username(request.form["token"])
        instance         = User(teacher_username, PATH + "/userman")
        college_group    = instance.college().group_name
        first_name       = request.form["first_name"].strip()
        last_name        = request.form["last_name"].strip()
        email            = request.form["email"].strip()
        team             = request.form["team"].strip()
        helpers.register_user(teacher_username, college_group, first_name, last_name, email, team)
        return "", 200
    return "", 403

@app.route("/user/<userid>", methods=["GET"])
def user_details(userid):
    if handle_authentication(request.args, userid):
        user = User(userid,PATH + "/userman")
        details = user.user_details()
        full_name = details["Full name"] + " " + details["Surname"]
        email     = details["E-mail"]
        return json.dumps({"full_name":full_name, "email":email}), 200
    return '{}', 403

@app.route("/user/<userid>", methods=["POST"])
def set_user_details(userid):
    if handle_authentication(request.form, userid):
        instance = User(userid, PATH + "/userman")
        if request.form.has_key("email"):
            instance.conn.set_user_attribute(userid, "mail", request.form["email"])
        if request.form.has_key("password"):
            instance.conn.set_user_password(userid, request.form["password"])
        return '{}', 200

    return '{}', 403

@app.route("/college", methods=["GET"])
def college_list():
    if handle_authentication(request.args):
        teacher_username = get_username(request.args["token"])
        instance = User(teacher_username, PATH + "/userman")
        college = instance.college()
        obj = {}
        obj["college_name"] = college.name()
        obj["userids"]      = college.users()
        obj["teams"]        = college.teams()
        return json.dumps(obj), 200

    return "{}", 403

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
