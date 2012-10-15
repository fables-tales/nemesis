import ldap
import ConfigParser
import subprocess
import os


def get_teachers(userman_path):
    process = ["./userman", "group", "members", "teachers"]
    p = subprocess.Popen(process, stdout=subprocess.PIPE, cwd=userman_path)
    p.wait()
    return p.stdout.read().split(" ")


def user_details(userman_path, userid):
    process = ["./userman", "user", "info", userid]
    p = subprocess.Popen(process, stdout=subprocess.PIPE, cwd=userman_path)
    p.wait()
    lines = p.stdout.read().strip().split("\n")
    results = {}
    for line in lines:
        key,value = line.split(": ")
        results[key] = value

    return results


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

    def get_user_details(self,userid):
        return user_details(self.userman_path, userid)


if __name__ == "__main__":
    assert LdapInstance().is_teacher("teacher_coll1") == True
