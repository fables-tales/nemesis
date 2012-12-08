import ldap
import ConfigParser
import subprocess
import hashlib
import base64

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

class LdapInstance:
    def __init__(self,userman_path="userman"):
        self.config = ConfigParser.SafeConfigParser()
        self.userman_path = userman_path
        self.config.readfp(open(userman_path + "/sr/config.ini"))
        self._ldap_connect()
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
        self._ldap_connect()
        bind_str = "cn=%s,o=sr" % self.config.get('ldap', 'username')
        password = self.config.get("ldap", "password")
        return self.conn.simple_bind_s(bind_str, password)

    def get_user_details(self,userid):
        return user_details(self.userman_path, userid)

    def get_college(self, userid):
        college = self._ldap_query_college_for_user(userid)
        if college == None:
            return None
        else:
            return College(college, self.userman_path)

    def is_teacher_of(self, teacherid, userid):
        c1 = self.get_college(teacherid)
        c2 = self.get_college(userid)
        return c1.group_name == c2.group_name

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

    def can_auth(self, username):
        return self.is_teacher(username) and self.get_college(username) is not None

    def _ldap_connect(self):
        self.conn = ldap.initialize("ldap://%s/" % self.config.get('ldap', 'host'))

    def _ldap_query_college_for_user(self, userid):
        self.manager_bind()
        query = self.conn.search_s("ou=groups,o=sr", ldap.SCOPE_SUBTREE, "(&(memberUid=" + userid + ")(cn=college*))", ["cn"])
        if len(query) == 1:
            return query[0][1]["cn"][0]
        else:
            return None



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


if __name__ == "__main__":
    assert LdapInstance().is_teacher("teacher_coll1") == True
