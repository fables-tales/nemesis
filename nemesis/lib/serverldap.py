import ldap
import json
import ConfigParser
import subprocess
import hashlib
import base64
import time
import os
import random

from hashlib import sha256
from helpers import sqlite_connect

PATH = os.path.dirname(os.path.abspath(__file__)) + "/../"

class College:
    def __init__(self, group_name, userman_path):
        self.group_name = group_name
        self.userman_path = userman_path

    def name(self):
        return college_name(self.userman_path, self.group_name)

    def teams(self):
        return college_teams(self.userman_path, self.group_name)

    def users(self):
        return group_members(self.userman_path, self.group_name)

class LdapConnection:
    def __init__(self, userman_path="userman"):
        self.config = ConfigParser.SafeConfigParser()
        print userman_path
        self.config.readfp(open(userman_path + "/sr/config.ini"))
        self._ldap_connect()

    def _ldap_connect(self):
        t = time.time()
        print "start ldap connect"
        self.conn = ldap.initialize("ldap://%s/" % self.config.get('ldap', 'host'))
        print "end ldap connect"
        print time.time() - t

    def bind(self, username, password):
        bind_str = "uid=" + username + ",ou=users,o=sr"

        try:
            self.conn.simple_bind_s(bind_str, password)
            print "bound succeeded"
            return True
        except ldap.INVALID_CREDENTIALS:
            return False

    def manager_bind(self):
        bind_str = "cn=%s,o=sr" % self.config.get('ldap', 'username')
        password = self.config.get("ldap", "password")
        return self.conn.simple_bind_s(bind_str, password)

    def set_user_attribute(self, user_id, attribute, new_value):
        self.manager_bind()
        bind_str = "uid=" + user_id + ",ou=users,o=sr"
        mod_attrs = [(ldap.MOD_REPLACE, attribute, str(new_value))]
        self.conn.modify_s(bind_str, mod_attrs)

    def set_user_password(self, user_id, password):
        self.manager_bind()

        bind_str = "uid=" + user_id + ",ou=users,o=sr"
        #string it
        password = str(password)
        modlist = [(ldap.MOD_REPLACE, "userPassword", encode_pass(password))]
        self.conn.modify_s(bind_str, modlist)

    def query(self, base, filter, attributes):
        self.manager_bind()
        return self.conn.search_s(base, ldap.SCOPE_SUBTREE, filter, attributes)

class User:
    def __init__(self, username, userman_path="userman"):
        self.username = username
        self.conn = LdapConnection(userman_path)
        self.userman_path = userman_path

    def is_teacher(self):
        return self.username in get_teachers(self.userman_path)

    def password_is_valid(self, password):
        return self.conn.bind(self.username, password)

    def user_details(self):
        return user_details(self.userman_path, self.username)

    def college(self):
        college = self._ldap_query_college_for_user(self.username)
        if college == None:
            return None
        else:
            return College(college, self.userman_path)

    def is_teacher_of(self, userid):
        c1 = self.college()
        c2 = User(userid, self.userman_path).college()
        return c1 is not None and c2 is not None and c1.group_name == c2.group_name

    def can_auth(self):
        return self.is_teacher() and self.college() is not None

    def _ldap_query_college_for_user(self, userid):
        query = self.conn.query("ou=groups,o=sr", "(&(memberUid=" + userid + ")(cn=college*))", ["cn"])
        if len(query) == 1:
            return query[0][1]["cn"][0]
        else:
            return None

    def authentication_response(self):
        if self.can_auth():
            auth_hash = {"token":self.make_token()}
            return json.dumps(auth_hash), 200
        elif not self.is_teacher():
            return '{"error": "not a teacher"}', 403
        elif self.college() is None:
            return '{"error": "not in a college"}', 403

    def make_token(self):
        token = str(sha256(str(random.randint(0,1000000))).hexdigest())
        c = sqlite_connect()
        cur = c.cursor()
        cur.execute("DELETE FROM auth WHERE token=?", (token,))
        cur.execute("INSERT INTO auth values (?,?)", (token, self.username))
        c.commit()
        return token


######INTERNAL CODE BELOW HERE.
######YOU ALMOST CERTAINLY CARE MORE ABOUT THE STUFF ABOVE

def encode_pass(p):
    h = hashlib.sha1(p)
    return "{SHA}%s" %( base64.b64encode( h.digest() ) )

def run_userman_task(task, userman_path):
    process = task
    p = subprocess.Popen(process, stdout=subprocess.PIPE, cwd=userman_path)
    p.wait()
    retcode = p.returncode
    if retcode != 0:
        raise "A userman task failed" + str(task)
    return p

def get_teachers(userman_path):
    p = run_userman_task(["./userman", "group", "members", "teachers"], userman_path)
    return p.stdout.read().strip().split(" ")


def user_details(userman_path, userid):
    p = run_userman_task(["./userman", "user", "info", userid], userman_path)
    lines = p.stdout.read().strip().split("\n")
    results = {}
    for line in lines:
        key,value = line.split(": ")
        results[key] = value

    return results

def group_members(userman_path, group):
    p = run_userman_task(["./userman", "group", "members", group], userman_path)
    return p.stdout.read().strip().split(" ")

def college_name(userman_path, college_group):
    college_group = college_group.replace("college-", "")
    p = run_userman_task(["./userman", "college", "info", college_group], userman_path)
    name = " ".join(p.stdout.read().strip().split("\n")[0].split(" ")[1:])
    return name

def college_teams(userman_path, college_group):
    college_group = college_group.replace("college-", "")
    p = run_userman_task(["./userman", "college", "info", college_group], userman_path)
    lines = p.stdout.read().strip().split("\n")
    team_lines = [x for x in lines if x.find("team") != -1]
    team_lines = [x.replace("\t - ", "") for x in team_lines]
    return team_lines

def get_username(token):
    c = sqlite_connect()
    cur = c.cursor()
    result = cur.execute("SELECT username FROM auth WHERE token=?", (token,))
    return result.next()[0]

def handle_authentication(args,userid=None):
    if args.has_key("token"):
        token = args["token"]
        teacher_username = get_username(token)
        user = User(teacher_username, PATH + "/userman")
        teacher = user.is_teacher()
        if userid is not None:
            return teacher and user.is_teacher_of(userid)
        else:
            return teacher

    return False


if __name__ == "__main__":
    assert User("teacher_coll1").is_teacher() == True
