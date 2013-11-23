#Nemesis REST API spec

##Version 3.4.0-alpha.2 [SemVer](http://semver.org/)

This document explains all the Nemesis API endpoints. The production version of
this API runs on http://studentrobotics.org/userman. URL components are of the
form `:something` represent URL parameters.

All response bodies are JSON objects, and their keys are explained in the
response body sections of each endpoint's specification.

All requests use http basic authentication to check if a user can authenticate
to an endpoint. If authentication details are missing or invalid then the
response of the request will be status code 403 with a json object containing
the key `authentication_errors` with a list of error codes in them. The error
codes are currently:

* `NO_USERNAME` if no username was provided
* `NO_PASSWORD` if no password was provided
* `WRONG_PASSWORD` if the user exists but the password is wrong

A 403 response from nemesis with no `authentication_errors` field represents
an authorization problem (the user authenticated successfully but is not
permitted to interact with the resource)

There are three user roles in nemesis:

* team-leader
* blueshirt
* student

The term "can administrate" in this document is used to determine whether or
not a user is capable of administrating another user. The conditions for this
are as follows:

* If the authenticated user is a team-leader in the same college as the user to
  be accessed they may access/modify information about that user so long as
  that user is not a blueshirt.
* If the authenticated user is a blueshirt in the same college as the user to
  be accessed they may access/modify information about that user so long as
  that user is not a blueshirt.
* An authenticated user can administrate itself

##GET /colleges

Gives a list of all colleges

####Parameters

None

####Response code

200 if the user authenticates successfully and is a blueshirt, else 403

####Response body

The object contains:

* `colleges`: a list of all the college ids


##GET /colleges/:id

Gives information about the college matching the `id` url parameter

####Parameters

None

####Response code

200 if the user authenticates successfully and is a member of the college,
200 if the user authenticates successfully and is a blueshirt
else 403.

####Response body

If the response code is 200 the object contains:

* `users`: A list of usernames in that college that the authenticated user can
           administrate. Example `['abc1']`. Only given if authentication has
           happened and the user is a member of this college.
* `teams`: a list of all the teams in that college. Example `['team-ABC']`.
* `college_name`: the name of the college.

##GET /user/:username

Gets information about the user specified in the URL parameter `username`.

####Parameters

No parameters

####Response code

200 if the user authenticates successfully and the authenticated user
can administrate the user specified by `:username`. 403 otherwise.

####Response body

If the response code is 200:

* `email`: the user's email address. Only given if the authenticated user
           is the user specified by :username or the authenticated user
           is a team-leader of the user specified by :username.
* `new_email`: the email address that the system has been asked to change
           to using. Only given if the authenticated user has access to the
           `email` field (see above) and a change request has been made.
* `username`: the user's username.
* `first_name`: the user's first name.
* `last_name`: the user's last name.
* `colleges`: a list of the colleges that the user is in.
* `teams`: a list of the teams that the user is in.
* `is_blueshirt`: a boolean indicating whether the user is a blueshirt.
* `is_student`: a boolean indicating whether the user is a student.
* `is_team_leader`: a boolean indicating whether the user is a team-leader.
* `has_media_consent`: a boolean indicating whether the user has given media consent.
* `has_withdrawn`: a boolean indicating whether the user has withdrawn.


##POST /user/:username

Updates information about the user specified in the URL parameter `username`.

####Parameters

* `new_email` optional: the new email address for the user. An update of the
  email is only performed if the authenticated user is the user specified by
:username or the authenticated user is a team-leader of the user specified by
:username. Changes to email address require validation. Change requests can
be cancelled by setting this to the users' current email.
* `new_team` optional: the new team for the user. An update of the team
  is only performed if:
  * the authenticated user is a team-leader of the user specified by :username,
  * and the authenticated user is a member of the new team,
  * and the user specified by :username is not a blueshirt.
* `new_password` optional: the new password for the user.
* `new_first_name` optional: the new first name for the user. Note that
    students are not permitted to update names, so this value will be ignored
    if the authenticated user is a student (the request will otherwise appear to succeed).
* `new_last_name` optional: the new last name for the user. Note that
    students are not permitted to update names, so this value will be ignored
    if the authenticated user is a student (the request will otherwise appear to succeed).
* `new_type` optional: the type of account (either `student` or `team-leader`). Note that
    only teachers can cause any update to this information, and cannot change themselves,
    so this value will be ignored if the authenticated user is a student or a teacher is
    trying to demote themselves. The request will appear to succeed.

####Response code

The same as the response code for `GET /user/:username`. No update is performed
if 403.

####Response body

The usual authentication error conditions apply, any other response data is
unspecified and should not be used.

##POST /registrations

Used to register new users. Specifically posting to this endpoint inserts one
user into the registration queue. The new user will be emailed to activate
their account, and the requesting user will be emailed a summary of the
new account's details.

####Parameters

* `first_name`: the user's first name.
* `last_name`: the user's last name.
* `email`: the user's email address.
* `college`: the college to register the user to.
* `team`: the team to register the user to.

####Response code

202 if the authenticated user is a member of the specified college and the
specified college has the specified team and the authenticated user is a
blueshirt or a team-leader and the requested user details are not already
in use. Otherwise 403.

####Response body

The usual authentication error conditions apply. Other errors are detailed
via a single `error` key in the returned json object. Its values possible
values are:

* `YOU_CANT_REGISTER_USERS`: The current user is not allowed to register
          users. Returned when the authenticated user is neither a
          team-leader nor a blueshirt.
* `BAD_COLLEGE`: The authenticated user is not a member of the requested
          college.
* `BAD_TEAM`: The requested team is not available within the requested college.
* `DETAILS_ALREADY_USED`: The name or email address requested for the user
          are already being used by another user.
