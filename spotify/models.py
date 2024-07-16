from datetime import date, datetime
import typing
from dataclasses import dataclass

import spotipy
from spotipy import SpotifyOAuth

if typing.TYPE_CHECKING:
    from itunes import IPlaylist


@dataclass
class SpotifyObject:
    sid: str

    @property
    def url(self):
        return f"https://open.spotify.com/{self.uri}"

    @property
    def embed(self):
        return f"https://open.spotify.com/embed/{self.uri}"

    @property
    def uri(self):
        return f"spotify:{self.__class__.__name__.lower()[1:]}:{self.sid}"


@dataclass
class STrack(SpotifyObject):
    name: str
    artist: str | list[str] | None
    album: str
    added_at: datetime
    release_date: date

    @property
    def url(self):
        return f"https://open.spotify.com/track/{self.sid}"

    @classmethod
    def from_tracks(cls, information: dict):
        try:
            release_date = None
            if information["track"]:
                match information["track"]["album"]["release_date_precision"]:
                    case "day":
                        release_date = datetime.strptime(information["track"]["album"]["release_date"], "%Y-%m-%d").date()
                    case "month":
                        release_date = datetime.strptime(information["track"]["album"]["release_date"], "%Y-%m").date()
                    case "year":
                        release_date = datetime.strptime(information["track"]["album"]["release_date"], "%Y").date()
                if information["track"]["artists"]:
                    return cls(information["track"]["id"], information["track"]["name"],
                               information["track"]["artists"][0]["name"] if len(information["track"]["artists"]) == 1 else [
                                   information["track"]["artists"][i]["name"] for i in
                                   range(len(information["track"]["artists"]))],
                               information["track"]["album"]["name"],
                               datetime.strptime(information["added_at"], "%Y-%m-%dT%H:%M:%SZ"),
                               release_date)
                else:
                    return cls(information["track"]["id"], information["track"]["name"],
                               None,
                               information["track"]["album"]["name"],
                               datetime.strptime(information["added_at"], "%Y-%m-%dT%H:%M:%SZ"),
                               release_date)
        except KeyError as e:
            print(e)


@dataclass
class SPlaylist(SpotifyObject):
    name: str
    description: str
    collaborative: bool
    tracks: list[STrack]
    itunes: bool = False
    reference: "IPlaylist" = None

    @property
    def url(self):
        return f"https://open.spotify.com/playlist/{self.sid}"

    def set_reference(self, reference):
        self.reference = reference
        self.itunes = True
        return self

    @classmethod
    def from_playlists(cls, information: dict, sp: spotipy.Spotify):
        tracks = []
        for track in sp.playlist_items(information["id"])["items"]:
            tracks.append(STrack.from_tracks(track))
        return cls(information["id"], information["name"], information["description"], information["collaborative"],
                   tracks)


class SLibrary:
    def __init__(self, client_id, client_secret, scopes=None):
        if scopes is None:
            scopes = ["playlist-read-private", "playlist-modify-public", "playlist-modify-private"]
        self._auth = self.authenticate(client_id, client_secret, scopes)
        self.sp = spotipy.Spotify(auth_manager=self._auth)
        self.playlists = []

    @staticmethod
    def authenticate(client_id, client_secret, scopes=None):
        return SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri='http://localhost:8888/callback',
                            scope=' '.join(scopes))

    def _get_authenticated_user_playlists(self):
        playlists = []
        results = self.sp.current_user_playlists()

        while results:
            playlists.extend(results['items'])
            if results['next']:
                results = self.sp.next(results)
            else:
                results = None

        return playlists

    @classmethod
    def parse_library(cls, client_id, client_secret, scopes=None):
        lib = cls(client_id, client_secret, scopes)
        playlists = lib._get_authenticated_user_playlists()
        print(len(playlists))
        for playlist in playlists:
            lib.playlists.append(SPlaylist.from_playlists(playlist, lib.sp))
        return lib


if __name__ == '__main__':
    library = SLibrary.parse_library(client_id='fdca1d7dfca94aff84921fb9166eaa2f',
                                     client_secret='da27bd3cab7349f3ad0844a826f0c7c0')
    print(len(library.playlists))
