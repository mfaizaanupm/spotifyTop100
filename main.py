import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
headers = {
    "CLIENT_ID" : "{your client_id}",
    "CLIENT_SECRET" : "{your client_secret}",
    "SPOTIPY_REDIRECT_URI":'http://example.com'
}
URL = "https://www.billboard.com/charts/hot-100/"


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=headers["CLIENT_ID"],
        client_secret=headers["CLIENT_SECRET"],
        show_dialog=True,
        cache_path="token.txt",
        username=headers["SPOTIPY_REDIRECT_URI"], 
    )
)
date = input("Which year would you like to travel to? (YYYY-MM-DD) ")

response = requests.get(URL + date)
soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name= f'{date} Billboard 100', public=False, collaborative=False, description='Top 100 from the day you were born')
sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=song_uris)
