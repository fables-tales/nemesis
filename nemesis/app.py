from flask import Flask, request
import json
import ldap
import userman.c_user as user
import ConfigParser
app = Flask(__name__)


import random
from hashlib import sha256


sessions = {}

class LdapInstance:
    def __init__(self):
        self.config = ConfigParser.SafeConfigParser()
        self.config.readfp(open("userman/sr/config.ini"))
        print self.config.get('ldap', 'host')
        self.conn = ldap.initialize("ldap://%s/" % self.config.get('ldap', 'host'))
        self.bound = False

    def bind(self, username, password):
        bind_str = "uid=" + username + ",ou=users,o=sr"
        print bind_str

        try:
            self.conn.simple_bind_s(bind_str, password)
            self.bound = True
            return True
        except ldap.INVALID_CREDENTIALS:
            return False

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
        if instance.bind(username, password):
            auth_hash = {"auth":sha256(str(random.randint(0,1000000))).hexdigest()}
            return json.dumps(auth_hash)
    return '', 403



if __name__ == "__main__":
    app.debug = True
    app.run()
