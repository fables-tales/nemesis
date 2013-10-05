
from datetime import datetime, timedelta

import helpers
import mailer

class UsernameKeyedSqliteThing(object):
    @classmethod
    def ListAll(cls, connector = None):
        connector = connector or helpers.sqlite_connect
        conn = connector()
        cur  = conn.cursor()

        rows = cur.execute('SELECT username FROM ' + cls._db_table)
        items = [cls(row[0], connector) for row in rows]
        return items

    _db_props = []

    def __init__(self, username, connector, auto_props = []):
        self._username = username
        self._connector = connector or helpers.sqlite_connect
        self._conn = None
        self._db_auto_props = auto_props
        self._props = {}
        self._in_db = False
        self._load()

    def __getattr__(self, name):
        if name not in self._db_props:
            raise AttributeError("No property '%s'" % (name))

        return self._props.get(name, None)

    def __setattr__(self, name, value):
        if name in self._db_props:
            self._props[name] = value
        else:
            self.__dict__[name] = value

    def _get_connection(self):
        if self._conn is None:
            self._conn = self._connector()
        return self._conn

    def _exec(self, statement, arguments):
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(statement, arguments)
        conn.commit()

    def _fetchone(self, statement, arguments):
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(statement, arguments)
        return cur.fetchone()

    def _load(self):
        props = self._db_props + self._db_auto_props
        statement = 'SELECT ' + ', '.join(props) + ' FROM ' + self._db_table + ' WHERE username=?'
        row = self._fetchone(statement, (self._username,))
        if not row is None:
            for i in xrange(len(props)):
                self._props[props[i]] = row[i]
            self._in_db = True

    def _missing_props(self):
        return [name for name in self._db_props if not self._props.has_key(name)]

    @property
    def username(self):
        return self._username

    @property
    def in_db(self):
        return self._in_db

    def delete(self):
        if not self.in_db:
            raise Exception( "Cannot remove pending user '%s' - not in database!" % (self.username,) )

        self._exec("DELETE FROM " + self._db_table + " WHERE username=?", (self.username,))
        self._in_db = False

    def save(self):
        missing = self._missing_props()
        if len(missing) > 0:
            missing_str = ', '.join(missing)
            raise Exception( "Cannot save user '%s' - missing settings: '%s'." % (self.username, missing_str) )

        if self.in_db:
            prep_statement = "UPDATE " + self._db_table + " SET " + '=?, '.join(self._db_props) + "=? WHERE username=?"
            self._exec(prep_statement, [self._props[x] for x in self._db_props] + [self.username])
        else:
            prep_statement = "INSERT INTO " + self._db_table + " (username, " + \
                             ', '.join(self._db_props) + ") VALUES (?" + \
                             ',?' * len(self._db_props) + ")"
            self._exec(prep_statement, [self.username] + [self._props[x] for x in self._db_props])
            self._in_db = True

class AgedUsernameKeyedSqliteThing(UsernameKeyedSqliteThing):

    def __init__(self, birth_time_prop, username, connector):
        super(AgedUsernameKeyedSqliteThing, self).__init__(username, connector, [birth_time_prop])
        self._birth_time_prop = birth_time_prop

    @property
    def age(self):
        if not self.in_db:
            return timedelta()
        else:
            rq_time = self._props[self._birth_time_prop]
            rq_time = datetime.strptime(rq_time, '%Y-%m-%d %H:%M:%S')
            age = datetime.utcnow() - rq_time
            return age

class PendingEmail(AgedUsernameKeyedSqliteThing):
    _db_table = 'email_changes'
    _db_props = ['new_email', 'verify_code']

    def __init__(self, username, connector = None):
        super(PendingEmail, self).__init__('request_time', username, connector)

    def send_verification_email(self, first_name, verification_url):
        email_vars = { 'name': first_name,
                        'url': verification_url }
        mailer.email_template(self.new_email, 'change_email', email_vars)

class PendingUser(AgedUsernameKeyedSqliteThing):
    _db_table = 'registrations'
    _db_props = ['teacher_username', 'college', 'team', 'email', 'verify_code']

    def __init__(self, username, connector = None):
        super(PendingUser, self).__init__('request_time', username, connector)

    def send_welcome_email(self, first_name, activation_url):
        email_vars = { 'name': first_name,
                   'username': self.username,
                      'email': self.email,
             'activation_url': activation_url
                     }

        mailer.email_template(self.email, 'new_user', email_vars)
