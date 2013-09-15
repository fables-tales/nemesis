
import smtplib
import os

from config import config

def email(toaddr, subject, msg):

    fromaddr = config.get('mailer', 'fromaddr')
    msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" % (fromaddr, toaddr, subject, msg)

    server = smtplib.SMTP(config.get('mailer', 'smtpserver'), timeout = 5)
    server.ehlo()
    server.starttls()
    server.ehlo()
    smtp_user = config.get('mailer', 'username')
    smtp_pass = config.get('mailer', 'password')
    server.login(smtp_user, smtp_pass)

    r = server.sendmail(fromaddr, toaddr, msg)

    try:
        server.quit()
    except smtplib.sslerror:
        pass

    return len(r) > 0

def email_template(toaddr, template_name, template_vars):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_path = os.path.join(script_dir, "templates", template_name + ".txt")

    msg = open(temp_path, 'r').read()

    subject = msg.splitlines()[0]
    assert subject[:8] == "Subject:"
    subject = subject[8:].strip()

    msg = "\n".join(msg.splitlines()[1:])
    msg = msg.format(**template_vars)

    return email(toaddr, subject, msg)

# In testing we don't want to actually send emails,
# so we write them out to files instead.
if not config.has_option('mailer', 'host'):
    import json
    from time import time
    def email(toaddr, subject, msg):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        name = 'mail-' + str(time()) + '.sent-mail'
        name = os.path.join(script_dir, name)
        with open(name, 'w') as f:
            args = { 'toaddr': toaddr
                   , 'subject': subject
                   , 'msg': msg
                   }
            json.dump(args, f)
