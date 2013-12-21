
import datetime
import httplib
import logging
import base64
import urllib
import sys
import os

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common_test_helpers import apache_mode, delete_db, get_registrations, assert_no_emails, last_email, last_n_emails, remove_user, root, template

def make_connection():
    if not apache_mode():
        return httplib.HTTPConnection("127.0.0.1",5000)
    else:
        return httplib.HTTPSConnection("localhost")

def modify_endpoint(endpoint):
    return "/userman" + endpoint if apache_mode() else endpoint

def unicode_encode(params_hash):
    for key in params_hash:
        params_hash[key] = params_hash[key].encode("utf-8")

def server_post(endpoint, params=None):
    conn = make_connection()
    endpoint = modify_endpoint(endpoint)
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}
    if params != None:
        if params.has_key("username") and params.has_key("password"):
            base64string = base64.encodestring('%s:%s' % (params["username"], params["password"])).replace('\n', '')
            headers["Authorization"] = "Basic %s" % base64string
            del params["username"]
            del params["password"]
        unicode_encode(params)
        url_params = urllib.urlencode(params)
        conn.request("POST", endpoint, url_params, headers)
    else:
        conn.request("POST", endpoint)

    resp = conn.getresponse()
    data = resp.read()
    return resp, data


def server_get(endpoint, params=None):
    conn = make_connection()
    endpoint = modify_endpoint(endpoint)
    headers = {}
    if params != None:
        if params.has_key("username") and params.has_key("password"):
            base64string = base64.encodestring('%s:%s' % (params["username"], params["password"])).replace('\n', '')
            headers["Authorization"] = "Basic %s" % base64string
            del params["username"]
            del params["password"]
        url_params = urllib.urlencode(params)
        conn.request("GET", endpoint, url_params, headers)
    else:
        conn.request("GET", endpoint)

    resp = conn.getresponse()
    data = resp.read()
    return resp, data
