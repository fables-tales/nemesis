#Nemesis REST API spec

##Version 3.0.0-1 [SemVer](http://semver.org/)

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

* teacher
* blueshirt
* student

Teachers and blueshirts may perform all operations on students in colleges they
are associated with. Students may read details about their college and
read/write their own details

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

200 if the user is authenticated, otherwise 403.

####Response body

If the response code is 200 the object contains:

* `userids`: a list of all the user ID's in that college. Example `['ab1']`.
             **Note**: this list includes teachers and students, but not blueshirts.
* `teams`: a list of all the teams in that college. Example `['team-ABC']`.
* `college_name`: the name of the college.

##GET /user/:userid

Gets information about the user specified in the URL parameter `userid`.

####Parameters

No parameters other than the authentication token.

####Response code

200 if the user is authenticated, otherwise 403.

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

200 if the user is authenticated and can modify the user with userid, otherwise
403.

####Response body

The response body is unspecified and should not be used.


##POST /user/register

Used to register new users. Specifically posting to this endpoint inserts one
user into the registration queue.

####Parameters

* `first_name`: the user's first name.
* `last_name`: the user's last name.
* `email`: the user's email address.
* `team`: the team to register the user to.

####Response code

200 if the user is authenticated and a teacher or blueshirt, otherwise 403.

####Response body

The response body is unspecified and should not be used.
