import os
import subprocess
from xml.etree import ElementTree as ET


def add_file_to_itunes_playlist(file_path, playlist_name):
    # Path to the VBScript file
    vbs_file_path = r'C:\Users\danie\PycharmProjects\pythonTesting\spotify-to-apple\to-itunes.vbs'

    # Command to run the VBScript with arguments
    command = ['cscript', vbs_file_path, file_path, playlist_name]

    # Execute the VBScript
    result = subprocess.run(command, capture_output=True, text=True)

    # Print the output from the VBScript
    return result.stdout.split('\n')[-2]


def parse_itunes_xml():
    tree = ET.parse(r"C:\Users\danie\Music\iTunes\iTunes Music Library.xml")
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
