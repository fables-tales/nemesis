
import sys
import os

def root():
   root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
   return root

sys.path.insert(0,os.path.join(root(), "nemesis/libnemesis"))
sys.path.insert(0,os.path.join(root(), 'nemesis'))

from sqlitewrapper import PendingEmail, PendingSend, sqlite_connect

from libnemesis import srusers

def apache_mode():
    return os.path.exists(".apachetest")

def delete_db():
    conn = sqlite_connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM registrations")
    cur.execute("DELETE FROM email_changes")
    cur.execute("DELETE FROM outbox")
    conn.commit()

def get_registrations():
    conn = sqlite_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM registrations")
    return list(cur)

def remove_user(name):
    """A setup helper"""
    def helper():
        u = srusers.user(name)
        if u.in_db:
            for gid in u.groups():
                g = srusers.group(gid)
                g.user_rm(u.username)
                g.save()
            u.delete()
    return helper

def last_email():
    conn = sqlite_connect()
    cur  = conn.cursor()
    cur.execute("SELECT id FROM outbox")
    row = cur.fetchone()
    assert row is not None, "Failed to get last email from SQLite."
    return PendingSend(row[0])

def last_n_emails(num):
    conn = sqlite_connect()
    cur  = conn.cursor()
    cur.execute("SELECT id FROM outbox LIMIT ?", (num,))
    rows = cur.fetchall()
    assert len(rows) == num, "Failed to get last %d emails from SQLite." % (num,)
    mails = []
    for row in rows:
        mails.append(PendingSend(row[0]))
    return mails

def assert_no_emails():
    conn = sqlite_connect()
    cur  = conn.cursor()
    cur.execute("SELECT id FROM outbox")
    row = cur.fetchone()
    assert row is None, "Should not be any emails in SQLite."

def template(name):
    file_path = os.path.join(root(), 'nemesis/templates', name)
    assert os.path.exists(file_path), "Cannot open a template that doesn't exist."
    with open(file_path, 'r') as f:
        return f.readlines()
