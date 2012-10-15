import httplib
import urllib
import sys
import os
sys.path.append(os.path.abspath('../nemesis/'))

def server_post(endpoint, params=None):
    conn = httplib.HTTPConnection("localhost:5000")
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}
    if params != None:
        url_params = urllib.urlencode(params)
        conn.request("POST", endpoint, url_params, headers)
    else:
        conn.request("POST", endpoint)

    return conn.getresponse()


def server_get(endpoint, params=None):
    conn = httplib.HTTPConnection("localhost:5000")
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}
    if params != None:
        url_params = urllib.urlencode(params)
        conn.request("GET", endpoint, url_params, headers)
    else:
        conn.request("GET", endpoint)

    return conn.getresponse()
