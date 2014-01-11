import os
import sys

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PATH + "/libnemesis/")

import subprocess
import logging
import json

import config
import mailer
import helpers
from helpers import log_action

from flask import Flask, request, url_for
from datetime import timedelta

from libnemesis import User, College, AuthHelper
from sqlitewrapper import PendingEmail, PendingUser

config.configure_logging()
app = Flask(__name__)


@app.route("/")
def index():
    return open(PATH + '/templates/index.html').read()

@app.route("/site/sha")
def sha():
    p = subprocess.Popen(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE, cwd=PATH)
    p.wait()
    return p.stdout.read()

@app.route("/registrations", methods=["POST"])
def register_user():
    ah = AuthHelper(request)
    if ah.auth_will_succeed:
        requesting_user = ah.user
        if requesting_user.can_register_users:
            teacher_username = requesting_user.username
            college_group    = request.form["college"].strip()
            first_name       = request.form["first_name"].strip()
            last_name        = request.form["last_name"].strip()
            email            = request.form["email"].strip()
            team             = request.form["team"].strip()

            if College(college_group) not in requesting_user.colleges:
                return json.dumps({"error":"BAD_COLLEGE"}), 403

            if team not in [t.name for t in College(college_group).teams]:
                return json.dumps({"error":"BAD_TEAM"}), 403

            if not helpers.is_email_valid(email):
                return json.dumps({"error":"BAD_EMAIL"}), 403

            if not helpers.is_name_valid(first_name):
                return json.dumps({"error":"BAD_FIRST_NAME"}), 403

            if not helpers.is_name_valid(last_name):
                return json.dumps({"error":"BAD_LAST_NAME"}), 403

            if User.name_used(first_name, last_name) or helpers.email_used(email):
                return json.dumps({"error":"DETAILS_ALREADY_USED"}), 403

            u = User.create_new_user(requesting_user, college_group, first_name, last_name)
            verify_code = helpers.create_verify_code(u.username, email)

            pu = PendingUser(u.username)
            pu.teacher_username = teacher_username
            pu.college = college_group
            pu.email = email
            pu.team = team
            pu.verify_code = verify_code
            pu.save()

            log_action('registering user', pu)

            url = url_for('activate_account', username=u.username, code=verify_code, _external=True)
            pu.send_welcome_email(first_name, url)

            rqu_email_vars = { 'name': requesting_user.first_name,
                      'pu_first_name': first_name,
                       'pu_last_name': last_name,
                        'pu_username': pu.username,
                         'pu_college': College(pu.college).name,
                           'pu_email': pu.email,
                            'pu_team': pu.team
                              }
            mailer.email_template(requesting_user.email, 'user_requested', rqu_email_vars)

            return "{}", 202
        else:
            return json.dumps({"error":"YOU_CANT_REGISTER_USERS"}),403
    else:
        return ah.auth_error_json, 403

@app.route("/user/<userid>", methods=["GET"])
def user_details(userid):
    ah = AuthHelper(request)
    if ah.auth_will_succeed and ah.user.can_administrate(userid):
        user = User.create_user(userid)
        details = user.details_dictionary_for(ah.user)
        email_change_rq = PendingEmail(user.username)
        if email_change_rq.in_db:
            new_email = email_change_rq.new_email
            if new_email != details['email']:
                details['new_email'] = new_email
        return json.dumps(details), 200
    else:
        return ah.auth_error_json, 403

def request_new_email(user, new_email):
    userid = user.username

    pe = PendingEmail(userid)

    if user.email == new_email:
        if pe.in_db:
            pe.delete()
        return

    verify_code = helpers.create_verify_code(userid, new_email)
    pe.new_email = new_email
    pe.verify_code = verify_code
    pe.save()

    url = url_for('verify_email', username=userid, code=verify_code, _external=True)
    pe.send_verification_email(user.first_name, url)

@app.route("/user/<userid>", methods=["POST"])
def set_user_details(userid):
    ah = AuthHelper(request)
    if ah.auth_will_succeed and ah.user.can_administrate(userid):
        user_to_update = User.create_user(userid)
        if request.form.has_key("new_email") and not ah.user.is_blueshirt:
            new_email = request.form["new_email"]
            request_new_email(user_to_update, new_email)
        # Students aren't allowed to update their own names
        # at this point, if the ah.user is valid, we know it's a self-edit
        if request.form.has_key("new_first_name") and not ah.user.is_student and request.form["new_first_name"] != '':
            user_to_update.set_first_name(request.form["new_first_name"])
        if request.form.has_key("new_last_name") and not ah.user.is_student and request.form["new_last_name"] != '':
            user_to_update.set_last_name(request.form["new_last_name"])
        if request.form.has_key("new_team"):
            team = request.form["new_team"]
            if (not user_to_update.is_blueshirt) and ah.user.manages_team(team):
                user_to_update.set_team(team)
        if request.form.has_key("new_type") and ah.user.is_teacher and user_to_update != ah.user:
            if request.form["new_type"] == 'student':
                user_to_update.make_student()
            elif request.form["new_type"] == 'team-leader':
                user_to_update.make_teacher()

        user_to_update.save()

        # Do this separately and last because it makes an immediate change
        # to the underlying database, rather than waiting for save().
        if request.form.has_key("new_password"):
            user_to_update.set_password(request.form["new_password"])

        return '{}', 200
    else:
        return ah.auth_error_json, 403

@app.route("/colleges", methods=["GET"])
def colleges():
    ah = AuthHelper(request)
    if ah.auth_will_succeed and ah.user.is_blueshirt:
        return json.dumps({"colleges":College.all_college_names()})
    else:
        return ah.auth_error_json,403

@app.route("/colleges/<collegeid>", methods=["GET"])
def college_info(collegeid):
    ah = AuthHelper(request)
    c = College(collegeid)
    if ah.auth_will_succeed and c in ah.user.colleges or ah.user.is_blueshirt:
        response = {}
        response["name"] = c.name
        response["teams"] = [t.name for t in c.teams]
        au = ah.user
        if c in au.colleges:
            response["users"] = [m.username for m in c.users if au.can_administrate(m)]

        return json.dumps(response), 200

    else:
        return ah.auth_error_json, 403

@app.route("/activate/<username>/<code>", methods=["GET"])
def activate_account(username, code):
    """
    Verifies to the system that an email address exists, and that the related
    account should be made into a full account.
    Expected to be used only by users clicking links in account-activation emails.
    Not part of the documented API.
    """

    pu = PendingUser(username)

    if not pu.in_db:
        return "No such user account", 404

    if pu.age > timedelta(days = 2):
        return "Request not valid", 410

    if pu.verify_code != code:
        return "Invalid verification code", 403

    log_action('activating user', pu)

    from libnemesis import srusers
    new_pass = srusers.users.GenPasswd()

    u = User(username)
    u.set_email(pu.email)
    u.set_team(pu.team)
    u.set_college(pu.college)
    u.set_password(new_pass)
    u.make_student()
    u.save()

    # let the team-leader know
    rq_user = User.create_user(pu.teacher_username)
    email_vars = { 'name': rq_user.first_name,
            'au_username': username,
          'au_first_name': u.first_name,
           'au_last_name': u.last_name
                 }
    mailer.email_template(rq_user.email, 'user_activated_team_leader', email_vars)

    pu.delete()

    html = open(PATH + "/templates/activate.html").read()
    replacements = { 'first_name': u.first_name
                   ,  'last_name': u.last_name
                   ,   'password': new_pass
                   ,      'email': u.email
                   ,   'username': username
                   ,       'root': url_for('.index')
                   }

    html = html.format(**replacements)

    return html, 200

@app.route("/verify/<username>/<code>", methods=["GET"])
def verify_email(username, code):
    """
    Verifies to the system that an email address exists, and assigns it to a user.
    Expected to be used only by users clicking links in email-verfication emails.
    Not part of the documented API.
    """

    change_request = PendingEmail(username)

    if not change_request.in_db:
        return "No such change request", 404

    if change_request.age > timedelta(days = 2):
        return "Request not valid", 410

    if change_request.verify_code != code:
        return "Invalid verification code", 403

    log_action('changing email', user = username, new_email = change_request.new_email)

    u = User(change_request.username)
    u.set_email(change_request.new_email)
    u.save()

    return "Email address successfully changed", 200

if __name__ == "__main__":
    # Run the app in debug mode
    app.debug = True
    app.run(host='0.0.0.0')
