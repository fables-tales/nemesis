import os
import sys

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PATH + "/libnemesis/")

import subprocess
import json
import helpers

from flask import Flask, request
from libnemesis import User, College

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
    requesting_user = User.from_flask_request(request)
    if requesting_user.can_register_users:
        teacher_username = requesting_user.username
        college_group    = request.form["college"].strip()
        if College(college_group) not in requesting_user.colleges:
            return "{}", 403
        first_name       = request.form["first_name"].strip()
        last_name        = request.form["last_name"].strip()
        email            = request.form["email"].strip()
        team             = request.form["team"].strip()
        if team not in [t.name for t in requesting_user.teams]:
            return "{}", 403
        helpers.register_user(teacher_username,
                college_group,
                first_name,
                last_name,
                email,
                team)
        return "{}", 200
    return "{}", 403

@app.route("/user/<userid>", methods=["GET"])
def user_details(userid):
    requesting_user = User.from_flask_request(request)
    if requesting_user.can_administrate(userid):
        user = User.create_user(userid)
        return json.dumps(user.details_dictionary), 200
    return '{}', 403

@app.route("/user/<userid>", methods=["POST"])
def set_user_details(userid):
    requesting_user = User.from_flask_request(request)
    if requesting_user.can_administrate(userid):
        instance = User.create_user(userid)
        if request.form.has_key("new_email"):
            instance.set_email(request.form["new_email"])
        if request.form.has_key("new_password"):
            instance.set_password(request.form["new_password"])
        if request.form.has_key("new_first_name"):
            instance.set_first_name(request.form["new_first_name"])
        if request.form.has_key("new_last_name"):
            instance.set_last_name(request.form["new_last_name"])

        instance.save()
        return '{}', 200

    return '{}', 403

@app.route("/colleges", methods=["GET"])
def user_colleges():
    requesting_user = User.from_flask_request(request)
    if requesting_user.is_authenticated():
        college_names = [str(x) for x in requesting_user.colleges]
        return json.dumps({"colleges":college_names}), 200
    else:
        return "{}", 403

@app.route("/colleges/<collegeid>", methods=["GET"])
def college_info(collegeid):
    c = College(collegeid)
    requesting_user = User.from_flask_request(request)
    if c in requesting_user.colleges:
        response = {}
        response["name"] = c.name
        response["users"] = [m.username for m in c.users if requesting_user.can_administrate(m)]
        response["teams"] = [t.name for t in c.teams]
        return json.dumps(response), 200
    else:
        return "{}", 403

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
