import os
import sys

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PATH + "/libnemesis/")

import subprocess
import json
import helpers

from flask import Flask, request
from libnemesis import User

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
        college_group    = requesting_user.colleges[0].name
        first_name       = request.form["first_name"].strip()
        last_name        = request.form["last_name"].strip()
        email            = request.form["email"].strip()
        team             = request.form["team"].strip()
        helpers.register_user(teacher_username,
                college_group,
                first_name,
                last_name,
                email,
                team)
        print "here"
        return "{}", 200
    return "{}", 403

@app.route("/user/<userid>", methods=["GET"])
def user_details(userid):
    requesting_user = User.from_flask_request(request)
    if requesting_user.can_administrate(userid):
        user = User.create_user(userid)
        return json.dumps(user.details_dictionary()), 200
    return '{}', 403

@app.route("/user/<userid>", methods=["POST"])
def set_user_details(userid):
    requesting_user = User.from_flask_request(request)
    if requesting_user.can_administrate(userid):
        instance = User.create_user(userid)
        if request.form.has_key("new-email"):
            instance.set_email(request.form["email"])
        if request.form.has_key("new-password"):
            instance.set_password(request.form["password"])

        instance.save()
        return '{}', 200

    return '{}', 403

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
