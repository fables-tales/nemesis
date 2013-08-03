import os
import sys

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PATH + "/libnemesis/")

import subprocess
import json
import helpers

from flask import Flask, request
from libnemesis import User, College, AuthHelper

app = Flask(__name__)


@app.route("/")
def index():
    return open(PATH + '/templates/index.html').read()

@app.route("/site/sha")
def sha():
    p = subprocess.Popen(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE, cwd=PATH)
    p.wait()
    return p.stdout.read()

@app.route("/registrations", methods=["POST"])
def register_user():
    ah = AuthHelper(request)
    if ah.auth_will_succeed:
        requesting_user = ah.user
        if requesting_user.can_register_users:
            teacher_username = requesting_user.username
            college_group    = request.form["college"].strip()
            first_name       = request.form["first_name"].strip()
            last_name        = request.form["last_name"].strip()
            email            = request.form["email"].strip()
            team             = request.form["team"].strip()

            if College(college_group) not in requesting_user.colleges:
                return json.dumps({"error":"BAD_COLLEGE"}), 403

            if team not in [t.name for t in College(college_group).teams]:
                return json.dumps({"error":"BAD_TEAM"}), 403

            helpers.register_user(teacher_username,
                    college_group,
                    first_name,
                    last_name,
                    email,
                    team)
            return "{}", 202
        else:
            return json.dumps({"error":"YOU_CANT_REGISTER_USERS"}),403
    else:
        return ah.auth_error_json, 403

@app.route("/user/<userid>", methods=["GET"])
def user_details(userid):
    ah = AuthHelper(request)
    if ah.auth_will_succeed and ah.user.can_administrate(userid):
        user = User.create_user(userid)
        return json.dumps(user.details_dictionary_for(ah.user)), 200
    else:
        return ah.auth_error_json, 403

@app.route("/user/<userid>", methods=["POST"])
def set_user_details(userid):
    ah = AuthHelper(request)
    if ah.auth_will_succeed and ah.user.can_administrate(userid):
        user_to_update = User.create_user(userid)
        if request.form.has_key("new_email") and not ah.user.is_blueshirt:
            user_to_update.set_email(request.form["new_email"])
        if request.form.has_key("new_password"):
            user_to_update.set_password(request.form["new_password"])
        if request.form.has_key("new_first_name"):
            user_to_update.set_first_name(request.form["new_first_name"])
        if request.form.has_key("new_last_name"):
            user_to_update.set_last_name(request.form["new_last_name"])
        if request.form.has_key("new_team"):
            team = request.form["new_team"]
            if not user_to_update.is_blueshirt and team in [t.name for t in ah.user.teams]:
                user_to_update.set_team(team)

        user_to_update.save()
        return '{}', 200
    else:
        return ah.auth_error_json, 403

@app.route("/colleges", methods=["GET"])
def colleges():
    ah = AuthHelper(request)
    if ah.auth_will_succeed and ah.user.is_blueshirt:
        return json.dumps({"colleges":College.all_college_names()})
    else:
        return ah.auth_error_json,403

@app.route("/colleges/<collegeid>", methods=["GET"])
def college_info(collegeid):
    ah = AuthHelper(request)
    c = College(collegeid)
    if ah.auth_will_succeed and c in ah.user.colleges or ah.user.is_blueshirt:
        response = {}
        response["name"] = c.name
        response["teams"] = [t.name for t in c.teams]
        au = ah.user
        if c in au.colleges:
            response["users"] = [m.username for m in c.users if au.can_administrate(m)]

        return json.dumps(response), 200

    else:
        return ah.auth_error_json, 403

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
