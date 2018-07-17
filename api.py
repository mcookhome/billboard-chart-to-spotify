""" Flask file to run my billdoard-to-spotify project as an API! """

import sys
import random
from flask import Flask, request
from urllib import quote
from billboard_to_spotify import run_with_auth_token 

api = Flask(__name__)

REDIRECT_URI = "http://mcook.me/billboard-to-spotify/callback"
SCOPE = "playlist-modify-public user-library-read user-read-email"
CLIENT_ID = "7ec9f8e4b6af41119d5029fa80ebf0b2"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"


auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    "show_dialog": "true",
    "client_id": CLIENT_ID
}

@api.route("/v1/authorization", methods=['GET'])
def authorize():
    """ Route to define my billboard-to-spotify page, handling get and post requests """
    
    url_args = "&".join(["{}={}".format(key,quote(val)) for key,val in auth_query_parameters.iteritems()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return auth_url

@api.route("/v1/bts", methods=['POST'])
def bts():
    print >>sys.stderr, str(request.form)
    print >>sys.stderr, request.form["auth_token"]
    chart = request.form["chart"]
    auth_token = request.form["auth_token"].encode('ascii', 'ignore')
    date = request.form["date"]
    run_with_auth_token(chart, date, auth_token) 
    

if __name__ == "__main__":
    api.run(debug=True)
