import json
import unittest

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class TestPlaylists(unittest.TestCase):
    def setUp(self):
        # Load the JSON scheme
        with open('scheme.json', 'r') as f:
            self.scheme = json.load(f)

        # Set up Spotify API client
        client_credentials_manager = SpotifyClientCredentials(
            client_id='fdca1d7dfca94aff84921fb9166eaa2f',
            client_secret='da27bd3cab7349f3ad0844a826f0c7c0'
        )
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_spotify_playlists_from_scheme(self, scheme):
        playlists = []
        for key, value in scheme.items():
            if isinstance(value, dict):
                playlists.extend(self.get_spotify_playlists_from_scheme(value))
            elif key == "spotify" and value:
                playlists.append(value)
        return playlists

    def test_all_playlists_in_spotify(self):
        scheme_playlists = self.get_spotify_playlists_from_scheme(self.scheme)
        for playlist_id in scheme_playlists:
            with self.subTest(playlist_id=playlist_id):
                try:
                    self.sp.playlist(playlist_id)
                except spotipy.exceptions.SpotifyException:
                    self.fail(f"Spotify playlist with ID {playlist_id} is not available")


if __name__ == '__main__':
    unittest.main()
