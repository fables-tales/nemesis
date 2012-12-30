#Nemesis REST API spec

##Version 3.0.0-3 [SemVer](http://semver.org/)

This document explains all the Nemesis API endpoints. It is assumed on most
requests that a `token` parameter is required. The token must be an API token
returned by the `/auth` endpoint. The production version of this API runs on
http://studentrobotics.org/userman. URL components of the form `:something`
represent URL parameters.

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

Team leaders may perform all operations on students in colleges they
are associated with. Students may read details about their college and
read/write their own details. Blueshirts may read/write their own details and
register students to colleges that they are associated with. One may be a team
leader and a blueshirt simultaneously, if so the team leader status takes
precedence.

##GET /colleges

Give a list of colleges the authenticated user is associated with.

####Parameters

No parameters other than the authentication token.

####Response code

200 if the user is authenticated, otherwise 403.

####Response body

If the response code is 200 the object contains:

* `colleges`: a list of all the college ids the authenticated user is associated
  with.


##GET /college/:id

Gives information about the college matching the `id` url parameter

####Parameters

No parameters other than the authentication token.

####Response code

200 if the user is authenticated and a member of the college, otherwise 403.

####Response body

If the response code is 200 the object contains:

* `userids`: a list of all the user ID's in that college. Example `['ab1']`.
             If the user is a team leader it will include **all** the student
             users in that college. If the user is a blueshirt or student it
             will only include that user.
* `teams`: a list of all the teams in that college. Example `['team-ABC']`.
* `college_name`: the name of the college.

##GET /user/:username

Gets information about the user specified in the URL parameter `username`.

####Parameters

No parameters other than the authentication token.

####Response code

200 if the user is authenticated and is the user specified by `username` or the
user is a team leader in the same college as the user specified by `username`
and the user specified by `username` is not a blueshirt, otherwise 403.

####Response body

If the response code is 200:

* `full_name`: the user's full name.
* `email`: the user's email address.


##POST /user/:username

Updates information about the user specified in the URL parameter `username`.

####Parameters

* `email` optional: the new email address for the user.
* `password` optional: the new password for the user.
* `first_name` optional: the new first name for the user.
* `last_name` optional: the new last name for the user.

####Response code

The same as the response code for `GET /user/:username`. No update is performed
if 403.

####Response body

The response body is unspecified and should not be used.


##POST /user/register

Used to register new users. Specifically posting to this endpoint inserts one
user into the registration queue.

####Parameters

* `first_name`: the user's first name.
* `last_name`: the user's last name.
* `email`: the user's email address.
* `college`: the college to register the user to.
* `team`: the team to register the user to.

####Response code

200 if the user is authenticated and a team leader or blueshirt and the team is
one associated with the college, otherwise 403.

####Response body

The response body is unspecified and should not be used.
