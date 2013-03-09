#Nemesis REST API spec

##Version 3.0.0-4 [SemVer](http://semver.org/)

This document explains all the Nemesis API endpoints. The production version of
this API runs on http://studentrobotics.org/userman. URL components are of the
form `:something` represent URL parameters.

All response bodies are JSON objects, and their keys are explained in the
response body sections of each endpoint's specification.

All requests take a `username` and `password` parameter. These are used to
perform authentication, and the response code will always be `403` if they do
not authenticate a user in ldap. The response body is an empty JSON object if
they do not authenticate a user.

There are three user roles in nemesis:

* team leader
* blueshirt
* student

The term "can administrate" in this document is used to determine whether or
not a user is capable of administrating another user. The conditions for this
are as follows:

* If the authenticated user is a team leader in the same college as the user to
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

200

####Response body

The object contains:

* `colleges`: a list of all the college ids


##GET /colleges/:id

Gives information about the college matching the `id` url parameter

####Parameters

No parameters are necessary, more information will be given however if a valid
username and password are given.

####Response code

200 if no username or password is given, 200 if the given username and password
are valid, else 403

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

200 if the the authentication parameters are valid and the authenticated user
can administrate the user specified by `:username`. 403 otherwise.

####Response body

If the response code is 200:

* `email`: the user's email address.
* `username`: the user's username.
* `first_name`: the user's first name.
* `last_name`: the user's last name.
* `colleges`: a list of the colleges that the user is in.


##POST /user/:username

Updates information about the user specified in the URL parameter `username`.

####Parameters

* `new_email` optional: the new email address for the user.
* `new_password` optional: the new password for the user.
* `new_first_name` optional: the new first name for the user.
* `new_last_name` optional: the new last name for the user.

####Response code

The same as the response code for `GET /user/:username`. No update is performed
if 403.

####Response body

The response body is unspecified and should not be used.

##POST /registrations

Used to register new users. Specifically posting to this endpoint inserts one
user into the registration queue.

####Parameters

* `first_name`: the user's first name.
* `last_name`: the user's last name.
* `email`: the user's email address.
* `college`: the college to register the user to.
* `team`: the team to register the user to.

####Response code

202 if the authenticated user is a member of the specified college and the
specified college has the specified team and the authenticated user is a
blueshirt or a team leader. Otherwise 403.

####Response body

The response body is unspecified and should not be used.
