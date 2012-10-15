import ldap
import ConfigParser
import subprocess
import hashlib
import base64


def encode_pass(p):
    h = hashlib.sha1(p)
    return "{SHA}%s" %( base64.b64encode( h.digest() ) )

def run_userman_task(task, userman_path):
    process = task
    p = subprocess.Popen(process, stdout=subprocess.PIPE, cwd=userman_path)
    p.wait()
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

def college_for_user(userman_path, userid):
    p = run_userman_task(["./userman", "group", "list"], userman_path)
    groups = p.stdout.read().strip().split("\n")
    colleges = [x for x in groups if x.find("college-") != -1]
    for college in colleges:
        if userid in group_members(userman_path, college):
            return college

def is_teacher_of(userman_path, teacher_id, student_id):
    teacher_college = college_for_user(userman_path, teacher_id)
    student_college = college_for_user(userman_path, student_id)
    return teacher_college == student_college

class LdapInstance:
    def __init__(self,userman_path="userman"):
        self.config = ConfigParser.SafeConfigParser()
        self.userman_path = userman_path
        self.config.readfp(open(userman_path + "/sr/config.ini"))
        self.conn = ldap.initialize("ldap://%s/" % self.config.get('ldap', 'host'))
        self.bound = False

    def is_teacher(self, username):
        return username in get_teachers(self.userman_path)

    def bind(self, username, password):
        bind_str = "uid=" + username + ",ou=users,o=sr"

        try:
            self.conn.simple_bind_s(bind_str, password)
            self.bound = True
            print "bound succeeded"
            return True
        except ldap.INVALID_CREDENTIALS:
            return False

    def manager_bind(self):
        self.conn = ldap.initialize("ldap://%s/" % self.config.get('ldap', 'host'))
        bind_str = "cn=%s,o=sr" % self.config.get('ldap', 'username')
        password = self.config.get("ldap", "password")
        return self.conn.simple_bind_s(bind_str, password)

    def get_user_details(self,userid):
        return user_details(self.userman_path, userid)

    def is_teacher_of(self, teacherid, userid):
        return is_teacher_of(self.userman_path, teacherid, userid)

    def set_user_attribute(self, user_id, attribute, new_value):
        self.manager_bind()

        bind_str = "uid=" + user_id + ",ou=users,o=sr"
        mod_attrs = [(ldap.MOD_REPLACE, attribute, str(new_value))]
        print mod_attrs
        self.conn.modify_s(bind_str, mod_attrs)

    def set_user_password(self, user_id, password):
        self.manager_bind()

        bind_str = "uid=" + user_id + ",ou=users,o=sr"
        #string it
        password = str(password)
        modlist = [(ldap.MOD_REPLACE, "userPassword", encode_pass(password))]
        self.conn.modify_s(bind_str, modlist)

if __name__ == "__main__":
    assert LdapInstance().is_teacher("teacher_coll1") == True
