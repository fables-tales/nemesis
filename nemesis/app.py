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
        print "woo"
        username = request.form["username"]
        password = request.form["password"]
        print username,password
        instance = LdapInstance()
        if instance.bind(username, password) and instance.is_teacher(username):
            auth_hash = {"auth":sha256(str(random.randint(0,1000000))).hexdigest()}
            return json.dumps(auth_hash)
    return '', 403



if __name__ == "__main__":
    app.debug = True
    app.run()
