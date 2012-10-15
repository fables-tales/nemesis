from flask import Flask, request
import json
app = Flask(__name__)
from hashlib import sha256
from serverldap import LdapInstance
import random


sessions = {}


@app.route("/auth", methods=["POST"])
def auth():
    print request.args
    print request.form
    if request.form.has_key("username") and request.form.has_key("password"):
        username = request.form["username"]
        password = request.form["password"]
        instance = LdapInstance()
        if instance.bind(username, password):
            if instance.is_teacher(username):
                auth_hash = {"token":sha256(str(random.randint(0,1000000))).hexdigest()}
                sessions[auth_hash["token"]] = (username, password)
                return json.dumps(auth_hash)
            else:
                return '{"error": "not a teacher"}', 403
        else:
            return '{"error": "invalid credentials"}', 403
    return '', 403


@app.route("/deauth", methods=["POST"])
def deauth():
    deleted = False
    if request.form.has_key("token"):
        token = request.form["token"]
        if sessions.has_key(token):
            del sessions[token]
            deleted = True


    if app.debug:
        return str(deleted), 200
    else:
        return '',200

@app.route("/user/<userid>", methods=["GET"])
def user_details(userid):
    print "gogo"
    if request.args.has_key("token"):
        print "got a token"
        token = request.args["token"]
        instance = LdapInstance()
        print sessions[token]
        if instance.bind(*sessions[token]) and instance.is_teacher(sessions[token][0])\
            and instance.is_teacher_of(sessions[token][0], userid):
            try:
                details = instance.get_user_details(userid)
                full_name = details["Full name"] + " " + details["Surname"]
                email     = details["E-mail"]
                return json.dumps({"full_name":full_name, "email":email}), 200
            except:
                return '["error":"an error occured"}', 500
    return '', 403


if __name__ == "__main__":
    app.debug = True
    app.run()
