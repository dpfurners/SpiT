import os
import time

from utils import *


scheme = load_scheme()
playlists = create_playlists_scheme(scheme)
sp_playlists, spotify = load_spotify_playlists()
it_playlists = parse_itunes_xml()

"""locations = [scheme["tanzen"]["all"], scheme["tanzen"]["special"],
             scheme["auflegen"]["extended"], scheme["auflegen"]["normal"],
             scheme["auflegen"]["normal"]["german"]]"""


if __name__ == '__main__':
    limit = 0
    not_downloadable = []

    download = {}
    for playlist, (spotify_id, itunes_playlist) in [(k, (s, i)) for k, (s, i) in playlists.items() if s and i]:
        print(f"Loading playlist: {playlist:>14} -> {itunes_playlist:<19} ({spotify_id:<22})", end="\r")
        songs = get_spotify_playlist_tracks(spotify, spotify_id)
        index = 0
        found = False
        for index, pl in enumerate(it_playlists):
            if pl["Name"] == itunes_playlist:
                found = True
                break
        if not found:
            print(f"Playlist {itunes_playlist}[{index}] not found in ITunes")
        pl_it_info = [{"name": track["Name"], "artist": track["Artist"]} for track in it_playlists[index]["Tracks"]]
        tracks = []
        for ind, song in enumerate(songs):
            if song not in pl_it_info:
                tracks.append((ind, song["name"]))
        if tracks:
            download[spotify_id] = tracks

    if limit:
        download = {k: v for i, (k, v) in enumerate(download.items()) if i < limit}
    if not download:
        print("No new songs to download")
        exit(0)

    progress_states = [
        {'description': f"{[k for k, (s, i) in playlists.items() if s == key][0]:>11}", 'progress': 0,
         'total': len(value), 'info': 'Resolved'}
        for key, value in download.items()
    ]

    progress = MultiLineProgress(progress_states)

    files = download_multiple(list(download.keys()), progress)

    for index, file in enumerate(files):
        progress.update_progress(index, 0, info="Extracting...")
        filename = file.split("\\")[-1].split("_")[0]
        location = rf"C:\Users\danie\Music\dp - Music\00 Downloads & Sortieren\auto\{filename}"
        extract_zip(file, location)
        progress.update_progress(index, progress.states[index]["total"], info="Extracted")
        playlist, tracks = list(download.items())[index]
        it_playlist = [x for i, x in playlists.values() if i == list(download.keys())[index]][0]
        progress.update_progress(index, 0, info="Adding to iTunes...")
        progress.update_total(index, len(tracks))
        added_tracks = []
        for track in os.listdir(location):
            if track.endswith(".mp3"):
                title = get_song_title(os.path.join(location, track))
                if title not in [sanitize_filename(x[1]) for x in tracks]:
                    continue
                add_file_to_itunes_playlist(os.path.join(location, track), it_playlist)
                added_tracks.append(track)
                progress.update_progress(index, progress.states[index]["progress"]+1, info="Added")
        # print(f"Added {len(os.listdir(location))} songs to {it_playlist}")
        progress.update_progress(index, progress.states[index]["total"], info="Finished")
        if len(added_tracks) != len(tracks):
            not_downloadable.append((playlist, [x[1] for x in tracks if x[1] not in added_tracks]))
        os.remove(file)
        time.sleep(2)
        # os.remove(location)
    progress.close()
    print("Not downloadable:")
    for playlist, tracks in not_downloadable:
        print(f"{playlist}: {', '.join(tracks)}")
