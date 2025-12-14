import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# LOAD .env FILE
load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
if not client_id or not client_secret:
    raise EnvironmentError("Missing Spotify credentials: set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET in .env")

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
)

def get_song_details(song):
    result = sp.search(q=song, type="track", limit=1)
    if result["tracks"]["items"]:
        t = result["tracks"]["items"][0]
        return {
            "name": t["name"],
            "artist": t["artists"][0]["name"],
            "image": t["album"]["images"][0]["url"],
            "preview": t["preview_url"]
        }
    return None
