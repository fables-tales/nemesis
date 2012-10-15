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


if __name__ == "__main__":
    app.debug = True
    app.run()
