import json
import utils

playlists = utils.load_spotify_playlists()

# Display playlist names and links
with open("scheme.json", "r") as f:
    scheme = json.load(f)

id_to_link = utils.id_to_link(playlists)

locations = [scheme["tanzen"]["all"], scheme["tanzen"]["special"],
             scheme["auflegen"]["extended"], scheme["auflegen"]["normal"],
             scheme["auflegen"]["normal"]["german"]]

for location in locations:
    location = utils.add_links(location, id_to_link)

with open("scheme_full.json", "w") as f:
    json.dump(scheme, f, indent=4)

soup = utils.get_itunes_info()
playlists = utils.extract_playlists(soup)
tracks = utils.extract_tracks(soup)

playlist_infos = []
for playlist in playlists:
    info = utils.extract_playlist_info(playlist)
    playlist_infos.append(info)
# Example of accessing playlists and tracks
for playlist in playlist_infos:
    try:
        if playlist["Name"] == "Library":
            continue
        print(f"Playlist: {playlist['Name']}")
    except KeyError:
        pass
    if "Tracks" in playlist:
        print("Tracks in this playlist:")
        for track_id in playlist["Tracks"]:
            track_info = tracks.get(track_id, {})
            print(f"  Track: {track_info['Name']}:{track_id}")