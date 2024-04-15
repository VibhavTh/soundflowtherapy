# Note we imported request!
from flask import Flask, render_template, request, redirect, session, url_for
from urllib.parse import quote
import requests
import json
import config
from vibhavhelper import moodfilter as filter
from vibhavhelper import helperfunctions as helper



app = Flask(__name__)

# set variables
#  Client Keys - TODO: Move these to a config file and set gitignore for the file.
CLIENT_ID =config.CLIENT_ID 
CLIENT_SECRET =config.CLIENT_SECRET 

app.secret_key = 'm%FWER]kl'

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)
# end of variables


# Set Server Env
CLIENT_SIDE_URL = config.CLIENT_SIDE_URL
# PORT = 5000
PORT = config.CLIENT_PORT
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)

#Set Scope for action on Spotify account
SCOPE = "playlist-modify-public playlist-read-collaborative user-library-read user-library-modify"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "scope": SCOPE
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/musictherapy')
def musictherapy():
    return render_template('musictherapy.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/surveyfeedback')
def surveyfeedback():
    return redirect("https://docs.google.com/forms/d/e/1FAIpQLSdRBFrm0dpjhfHnRX_8gHHog_qeugY-FyxGH8cU9e9KPZCpoQ/viewform?usp=sf_link")

# This page will have the sign up form
@app.route('/musictool')
def musictool():
    return render_template('musictool.html')

def get_authorization():
     # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

@app.route('/processchoice', methods=['POST'])
def processchoice():
    mode = request.form['mode']
    mood = request.form.get('mood', '')  # Optional, mood may not be present if 'random' mode is selected
    if mood == "":
        mood = helper.get_random_mood()
    session['mode'] = mode
    session['mood'] = mood

    return get_authorization()

@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    session["AUTH_TOKEN"] = auth_token
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
   
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)

    profile_data = json.loads(profile_response.text)
    display_name = profile_data["display_name"]
    user_id = profile_data["id"]
   
    #create playlist
    user_playlists_api_end_point = "https://api.spotify.com/v1/users/{}/playlists".format(user_id)
    mood = session['mood']
    mode =   session['mode'] 
    # playlist_name = display_name +"-"+ mood+ "playlist"+ helper.create_playlist_name()
    playlist_name = mood.capitalize() + " Playlist "+ helper.create_playlist_name()
    
    playlist_description = "A special playlist created for " + display_name 
    
    request_body = json.dumps({
          "name": playlist_name,
          "description": playlist_description,
          "public": True 
        })
 
    response = requests.post(url = user_playlists_api_end_point, data = request_body, headers={"Content-Type":"application/json", 
                        "Authorization": "Bearer {}".format(access_token)})

    response_json = response.json()
  
    playlist_uri = response_json['external_urls']['spotify']
    playlist_id= response_json['id']
   
    # Add songs to the playlist
    add_tracks_end_point="https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
    tracks_to_add = filter.getPlaylistSongs(mood)
    request_body = json.dumps({"uris": tracks_to_add, "position": 0 })
    snapshot_id = requests.post(url = add_tracks_end_point, data = request_body, headers={"Content-Type":"application/json", 
                        "Authorization": "Bearer {}".format(access_token)})

    snapshot_id = snapshot_id.json()

    session['mode'] = None
    session['mood']= None
  
    return render_template('thankyou.html', display_name=display_name, playlist_uri=playlist_uri, playlist_name=playlist_name, mood=mood, userchoice=mode)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
