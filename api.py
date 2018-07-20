""" Flask file to run my billdoard-to-spotify project as an API! """

import sys
import random
from flask import Flask, request
from urllib import quote
from billboard_to_spotify import run_with_access_token 
from credentials import get_secret
import base64
import requests
import json

api = Flask(__name__)

REDIRECT_URI = "http://mcook.me/billboard-to-spotify/callback"
SCOPE = "playlist-modify-public user-library-read user-read-email"
CLIENT_ID = "7ec9f8e4b6af41119d5029fa80ebf0b2"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"


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
    """ Route to create a Spotify URL that will lead users to an authorization page """
    
    url_args = "&".join(["{}={}".format(key,quote(val)) for key,val in auth_query_parameters.iteritems()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return auth_url

@api.route("/v1/gain-access", methods=['POST'])
def access():
    """ Route to get an access token from Spotify """

    auth_token = request.form["auth_token"]
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, get_secret()))
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]
    return access_token

@api.route("/v1/bts", methods=['POST'])
def bts():
    """ Route to expose my billboard-to-spotify program, handling post requests """

    chart = request.form["chart"]
    access_token = request.form["access_token"]
    date = request.form["date"] 
    playlist_url = run_with_access_token(chart, date, access_token) 
    return playlist_url

if __name__ == "__main__":
    api.run(debug=True)
