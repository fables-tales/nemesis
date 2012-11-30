#Nemesis REST API spec

##Version 2.0.0 [SemVer](http://semver.org/)

This document explains all the Nemesis API endpoints. It is assumed on most
requests that a `token` parameter is required. The token must be an API token
returned by the `/auth` endpoint. The production version of this API runs on
http://studentrobotics.org/userman. URL components of the form `:something`
represent URL parameters.

All response bodies are JSON objects, and their keys are explained in the
response body sections of each endpoint's specification.


##POST /auth

Authenticates users.

####Parameters

* `username`: the username of the user trying to authenticate.
* `password`: the password of the user trying to authenticate.

####Response code

200 if the username and password match a user and password combination in LDAP
and the user is a team leader. 403 otherwise.

####Response body

If the response code is 200:

* `token`: an authentication token for the rest of the Nemesis API.

If the response code is 403:

* `error`: a string error code explaining the error to to the user, one of:
    * `not a teacher`: given if the user is not a teacher.
    * `invalid credentials`: given if the user's credentials are wrong.


##POST /deauth

Deauthenticates existing authentication tokens.

####Parameters

* `token`: an authentication token for the rest of the Nemesis API.

####Response code

Always 200.

####Response body

If the API is in debug mode:

* `deleted`: `true` if the token existed and has been deleted, `false`
  otherwise.

If the API is in production mode the response body is always empty.


##GET /college

Gets information about the currently authenticated user's college.

####Parameters

No parameters other than the authentication token.

####Response code

200 if the user is authenticated, otherwise 403.

####Response body

If the response code is 200:

* `userids`: a list of all the user ID's in that college. Example `['ab1']`.
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


##POST /user/:userid

Updates information about the user specified in the URL parameter `userid`.

####Parameters

* `email` optional: the new email address for the user.
* `password` optional: the new password for the user.

####Response code

200 if the user is authenticated, otherwise 403.

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

200 if the user is authenticated, otherwise 403.

####Response body

The response body is unspecified and should not be used.


##GET /site/sha

Gets the current Git revision of the running site.

####Parameters

No parameters at all, this endpoint is not authenticated.

####Response code

Always 200.

####Response body

**This response body is not a JSON object**. The current Git revision hash
corresponding to the checked out and running version of the API service.
