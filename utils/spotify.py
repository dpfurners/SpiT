import spotipy
from spotipy.oauth2 import SpotifyOAuth


def load_spotify_playlists():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='fdca1d7dfca94aff84921fb9166eaa2f',
                                                   client_secret='da27bd3cab7349f3ad0844a826f0c7c0',
                                                   redirect_uri='http://localhost:8888/callback',
                                                   scope='playlist-read-private'))

    # Get current user's playlists
    playlists = sp.current_user_playlists()
    return playlists, sp


def get_spotify_playlists_from_scheme(scheme):
    playlists = []
    for key, value in scheme.items():
        if isinstance(value, dict):
            playlists.extend(get_spotify_playlists_from_scheme(value))
        elif key == "spotify" and value:
            playlists.append(value)
    return playlists


def get_spotify_playlist_tracks(sp, playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = []
    for item in results['items']:
        track = item['track']
        artists = [artist['name'] for artist in track['artists']]
        track_info = {
            'name': track['name'],
            'artist': "/".join(artists),
        }
        tracks.append(track_info)
    return tracks

