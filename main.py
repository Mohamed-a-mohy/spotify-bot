from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

date_wanted = input("type the date u want to get a list for in form of YYYY-MM-DD: ")

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_S = os.environ["CLIENT_S"]
SPOTIPY_REDIRECT_URI = "http://example.com"


html_doc = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date_wanted}/")
soup = BeautifulSoup(html_doc.text, 'html.parser')
top_100_list = [i.getText() for i in soup.find_all(name="h3",class_="a-no-trucate")]


sp = spotipy.oauth2.SpotifyOAuth(client_secret=CLIENT_S,client_id=CLIENT_ID, redirect_uri=SPOTIPY_REDIRECT_URI,scope="playlist-modify-private")

sp_user = spotipy.Spotify(client_credentials_manager=sp).current_user()
print(sp_user['id'])
user_id = sp_user['id']


playlist_creation = spotipy.Spotify(client_credentials_manager=sp).user_playlist_create(user=user_id, name=f"{date_wanted} billboard list ", public=False)
playlist_id = playlist_creation["id"]


songs_uri_list = []
for song in top_100_list:
    result = spotipy.Spotify(client_credentials_manager=sp).search(q=f"track:{song} year:{date_wanted[:4]}", type="track")

    if result["tracks"]["items"][0]["uri"]:
        songs_uri_list.append(result["tracks"]["items"][0]["uri"])


add_list = spotipy.Spotify(client_credentials_manager=sp).playlist_add_items(playlist_id, songs_uri_list)


