import os
import subprocess
import json

from serverldap import LdapInstance
from helpers import sqlite_connect, handle_authentication, get_username
from flask import Flask, request

import helpers

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

@app.route("/css/bootstrap.css")
def bootstrap_css():
    return open(PATH + "/static/css/bootstrap.css").read()

@app.route("/js/main.js")
def javascript():
    return open(PATH + "/static/js/main.js").read()

@app.route("/auth", methods=["POST"])
def auth():
    if request.form.has_key("username") and request.form.has_key("password"):
        username = request.form["username"]
        password = request.form["password"]
        instance = LdapInstance(PATH + "/userman")
        if instance.bind(username, password):
            if instance.is_teacher(username) and instance.get_college(username) is not None:
                auth_hash = {"token":helpers.make_token(username)}
                return json.dumps(auth_hash)
            elif not instance.is_teacher(username):
                return '{"error": "not a teacher"}', 403
            elif instance.get_college(username) is None:
                return '{"error": "not in a college"}', 403
        else:
            return '{"error": "invalid credentials"}', 403
    return '', 403


@app.route("/deauth", methods=["POST"])
def deauth():
    deleted = False
    if request.form.has_key("token"):
        token = request.form["token"]
        c = sqlite_connect()
        cur = c.cursor()
        cur.execute("DELETE FROM auth WHERE token=?", (token,))
        c.commit()

        if c.total_changes == 1:
            deleted = True
        else:
            deleted = False

    if app.debug:
        return str(deleted), 200
    else:
        return '',200

@app.route("/user/register", methods=["POST"])
def register_user():
    if handle_authentication(request.form):
        instance         = LdapInstance(PATH + "/userman")
        teacher_username = get_username(request.form["token"])
        college_group    = instance.get_college(teacher_username)
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
        instance = LdapInstance(PATH + "/userman")
        try:
            details = instance.get_user_details(userid)
            full_name = details["Full name"] + " " + details["Surname"]
            email     = details["E-mail"]
            return json.dumps({"full_name":full_name, "email":email}), 200
        except:
            return '["error":"an error occured"}', 500
    return '{}', 403

@app.route("/user/<userid>", methods=["POST"])
def set_user_details(userid):
    if handle_authentication(request.form, userid):
        instance = LdapInstance(PATH + "/userman")
        if request.form.has_key("email"):
            instance.set_user_attribute(userid, "mail", request.form["email"])
        if request.form.has_key("password"):
            instance.set_user_password(userid, request.form["password"])
        return '{}', 200

    return '{}', 403

@app.route("/college", methods=["GET"])
def college_list():
    if handle_authentication(request.args):
        instance = LdapInstance(PATH + "/userman")
        teacher_username = get_username(request.args["token"])
        college_group = instance.get_college(teacher_username)
        college_name  = instance.get_college_name(college_group)
        college_users = instance.get_group_users(college_group)
        college_teams = instance.get_college_teams(college_group)
        obj = {}
        obj["college_name"] = college_name
        obj["userids"] = college_users
        obj["teams"] = college_teams
        return json.dumps(obj), 200

    return "{}", 403

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
