from bs4 import BeautifulSoup
import requests
import argparse
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

SPOTIPY_CLIENT_ID = "8cae55eb53274659a5771e5496dfc226"
SPOTIPY_CLIENT_SECRET = "30d8e4cbae6a4d0693a9248becc2cd06"
SPOTIPY_REDIRECT_URI = 'http://example.com'  # 必須在Spotify Developer Dashboard中設定的回調URI
USERNAME = "317zyyevb5zyyuaqdkaxgbd6smfi"

scope = 'playlist-modify-private'  # 你的應用程式需要的權限

# 建立 SpotifyOAuth 物件
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope,
                                               cache_path = "token.txt", 
                                               username = USERNAME, 
                                               show_dialog = True))

# 取得使用者授權
auth_url = sp.auth_manager.get_authorize_url()
print(auth_url)

token = sp.auth_manager.get_access_token()

user_id = sp.current_user()["id"]




# date = input("Which year do want to travel to? Type the date in the format YYYY-MM-DD: ")
date = "2023-01-02"
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
soup = BeautifulSoup(response.text, "html.parser")

list = soup.select("div ul li ul li h3")
    
title_list = [song.getText().strip() for song in list][0:5:1]
print(title_list)


year = str(date).split("-")[0]
track_uri_list = []
for song in title_list:
    track = sp.search(q=f"track:{song}, year:{year}", type='track')
    if track['tracks']['items']:
        track_uri = track['tracks']['items'][0]["uri"]
        # print(track_id)
        track_uri_list.append(track_uri)
    else:
        track_uri_list.append("skipped")
        
playlist = sp.user_playlist_create(user_id, "Billboard 100 ha ha", public=False, description= "Ha")
playlist_id = playlist["id"]

valid_playlist = [track for track in track_uri_list if track != "skipped"]
print(valid_playlist)
sp.user_playlist_add_tracks(user= user_id, playlist_id= playlist_id, tracks = valid_playlist)
# pprint.pprint(playlist)
playlist_items = sp.playlist_items(playlist_id)
pprint.pprint(playlist_items["items"])