import bs4
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def load_spotify_playlists():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='fdca1d7dfca94aff84921fb9166eaa2f',
                                                   client_secret='da27bd3cab7349f3ad0844a826f0c7c0',
                                                   redirect_uri='http://localhost:8888/callback',
                                                   scope='playlist-read-private'))

    # Get current user's playlists
    playlists = sp.current_user_playlists()
    return playlists


def id_to_link(playlists):
    id_to_link = {}
    for playlist in playlists['items']:
        id_to_link[playlist["id"]] = playlist["external_urls"]["spotify"]
    return id_to_link


def add_links(location, id_to_link):
    for playlist in location:
        try:
            identification = location[playlist]["spotify"]
            link = id_to_link[identification]
            location[playlist]["link"] = link
        except KeyError:
            print(f"Playlist {playlist} not found in Spotify")
    print(f"Added links to {location}")
    return location


def get_itunes_info():
    with open(r"C:\Users\danie\Music\iTunes\iTunes Music Library.xml", "r", encoding="utf-8") as f:
        soup = bs4.BeautifulSoup(f, "xml", from_encoding="utf-8")
    return soup


def extract_playlists(soup):
    playlists = []
    for plist in soup.find_all("dict"):
        for key in plist.find_all("key"):
            if key.string == "Playlists":
                playlists.extend(key.find_next_sibling("array").find_all("dict"))
    return playlists


def extract_playlist_info(playlist):
    playlist_info = {}
    for element in playlist.find_all("key"):
        if element.string == "Name":
            playlist_info["Name"] = element.find_next_sibling("string").string
        elif element.string == "Playlist Items":
            playlist_info["Tracks"] = [item.find("key").find_next_sibling("integer").string for item in
                                       element.find_next_sibling("array").find_all("dict")]
    return playlist_info


def extract_tracks(soup):
    tracks = {}
    for dict_tag in soup.find_all("dict"):
        for key in dict_tag.find_all("key"):
            if key.string == "Tracks":
                track_elements = key.find_next_sibling("dict").find_all("dict")
                for track in track_elements:
                    track_id = track.find("key", text="Track ID").find_next_sibling("integer").string
                    track_info = {}
                    for tag in track.find_all("key"):
                        if tag.string and tag.string not in ["Track ID"]:
                            value = tag.find_next_sibling()
                            track_info[tag.string] = value.string if value else None
                    tracks[track_id] = track_info
    return tracks
