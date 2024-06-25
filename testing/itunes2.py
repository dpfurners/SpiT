import xml.etree.ElementTree as ET


def parse_itunes_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    playlists = []
    tracks = {}

    # Extract tracks
    for dict_entry in root.findall("./dict/dict/dict"):
        track_id = None
        track_info = {}

        for i in range(0, len(dict_entry), 2):
            key = dict_entry[i].text
            value = dict_entry[i + 1].text
            if key == "Track ID":
                track_id = value
            else:
                track_info[key] = value

        if track_id:
            tracks[track_id] = track_info

    # Extract playlists and their tracks
    for playlist in root.findall("./dict/array/dict"):
        playlist_name = None
        track_ids = []

        for i in range(0, len(playlist), 2):
            key = playlist[i].text
            value = playlist[i + 1]

            if key == "Name":
                playlist_name = value.text
            elif key == "Playlist Items":
                for item in value.findall("dict"):
                    for j in range(0, len(item), 2):
                        if item[j].text == "Track ID":
                            track_ids.append(item[j + 1].text)

        if playlist_name:
            playlists.append({
                "Name": playlist_name,
                "Tracks": [tracks[track_id] for track_id in track_ids if track_id in tracks]
            })

    return playlists


def check_song_in_specific_playlist(playlists, target_playlist_name, song_name, song_artist):
    for playlist in playlists:
        if playlist['Name'] == target_playlist_name:
            for track in playlist['Tracks']:
                if track.get('Name', '') == song_name and track.get('Artist', '') == song_artist:
                    return True
    return False


def main():
    xml_path = r'C:\Users\danie\Music\iTunes\iTunes Music Library.xml'

    # Parse the iTunes XML file
    playlists = parse_itunes_xml(xml_path)

    # Example Spotify song details to check
    target_playlist_name = 'House-'
    spotify_song_name = "Don't Trust Me - Matthew Topper In My Room Edit (Dirty)"
    spotify_song_artist = '3OH!3'

    # Check if the song is already in the specific playlist
    if check_song_in_specific_playlist(playlists, target_playlist_name, spotify_song_name, spotify_song_artist):
        print(
            f'The song "{spotify_song_name}" by "{spotify_song_artist}" is already in the playlist "{target_playlist_name}".')
    else:
        print(
            f'The song "{spotify_song_name}" by "{spotify_song_artist}" is not in the playlist "{target_playlist_name}".')


if __name__ == '__main__':
    main()
