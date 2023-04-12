from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# The Last.fm API endpoint for getting top artists
ARTISTS_API_URL = 'http://ws.audioscrobbler.com/2.0/'

# The Last.fm API endpoint for getting top tracks
TRACKS_API_URL = 'http://ws.audioscrobbler.com/2.0/'

# The Last.fm API key
API_KEY = '0757b79145c7dab3d5143d851d4a1618'

# The number of top artists to retrieve
NUM_ARTISTS = 5

# The number of top tracks to retrieve
NUM_TRACKS = 5

# This function retrieves the top artists for a given country using the Last.fm API
def get_top_artists(country):
    params = {
        'method': 'geo.gettopartists',
        'country': country,
        'api_key': API_KEY,
        'limit': NUM_ARTISTS,
        'format': 'json'
    }
    response = requests.get(ARTISTS_API_URL, params=params)
    response_json = response.json()
    top_artists = []
    for artist in response_json['topartists']['artist']:
        top_artists.append(artist['name'])
    return top_artists

# This function retrieves the top tracks for a given country using the Last.fm API
def get_top_tracks(country):
    params = {
        'method': 'geo.gettoptracks',
        'country': country,
        'api_key': API_KEY,
        'limit': NUM_TRACKS,
        'format': 'json'
    }
    response = requests.get(TRACKS_API_URL, params=params)
    response_json = response.json()
    top_tracks = []
    for track in response_json['tracks']['track']:
        top_tracks.append(track['name'] + ' - ' + track['artist']['name'])
    return top_tracks

# This is the main route for the web app, where users can input a country name
@app.route('/', methods=['GET', 'POST'])
def get_top_artists_and_songs():
    if request.method == 'POST':
        country = request.form['country']
        top_artists = get_top_artists(country)
        top_tracks = get_top_tracks(country)
        return render_template('index.html', top_artists=top_artists, top_tracks=top_tracks)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)