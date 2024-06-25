import json
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


def get_song_title(file_path):
    try:
        audio = MP3(file_path, ID3=EasyID3)
        return audio['title'][0] if 'title' in audio else None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def load_scheme():
    with open("scheme.json", "r") as f:
        return json.load(f)


def create_playlists_scheme(scheme):
    playlists = {}

    def recurse_scheme(scheme, parent_name=""):
        for key, value in scheme.items():
            if isinstance(value, dict):
                if 'spotify' in value and 'itunes' in value:
                    playlists[key] = (value['spotify'], value['itunes'])
                else:
                    recurse_scheme(value, key)

    recurse_scheme(scheme)
    return playlists

