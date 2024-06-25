import json
import os
import win32com.client

# Path to the JSON schema
schema_path = 'scheme.json'

# Load the JSON schema from the file
with open(schema_path, 'r') as file:
    schema = json.load(file)

# Path to the song you want to add
song_path = r"C:\Users\danie\Music\Hello.mp3"

# Name of the playlist to which you want to add the song
target_playlist_name = "House-"

# Create an instance of iTunes
itunes = win32com.client.Dispatch("iTunes.Application")


# Function to check if a playlist exists in iTunes and return it
def get_playlist(playlist_name):
    playlists = itunes.LibrarySource.Playlists
    for playlist in playlists:
        if playlist.Name == playlist_name:
            return playlist
    return None


# Function to add a song to a specific playlist
def add_song_to_playlist(song_path, playlist):
    if not os.path.exists(song_path):
        print(f"File not found: {song_path}")
        return

    try:
        # Add the song to the iTunes library
        print(f"Adding song to iTunes library: {song_path}")
        operation_status = itunes.LibraryPlaylist.AddFile(song_path)

        # Check if operation_status is None or not
        if operation_status is None:
            print("Failed to add song to the iTunes library.")
            return

        # Debug: Print the type and properties of the operation_status object
        print(f"OperationStatus object type: {type(operation_status)}")
        print(f"OperationStatus object properties: {dir(operation_status)}")

        # Ensure Tracks property can be accessed
        try:
            tracks = operation_status.Tracks
            print(f"Tracks object type: {type(tracks)}")
            print(f"Tracks object properties: {dir(tracks)}")

            # Assuming single track addition, get the first track
            track = tracks.Item(1)
            track_name = track.Name
            track_artist = track.Artist
            print(f"Song added to iTunes library: {track_name} by {track_artist}")
        except Exception as e:
            print(f"Failed to access track properties: {e}")
            return

        # Add the track to the target playlist using the proper method
        print(f"Adding track to playlist: {playlist.Name}")
        playlist.AddTrack(track)
        print(f"Song added successfully to '{playlist.Name}': {track.Name} by {track.Artist}")

    except Exception as e:
        print(f"An error occurred while adding the song: {e}")


# Check for the specific playlist in the schema
def find_playlist_in_schema(schema, target_playlist_name):
    for key, value in schema.items():
        if isinstance(value, dict):
            result = find_playlist_in_schema(value, target_playlist_name)
            if result:
                return result
        elif key == 'itunes' and value == target_playlist_name:
            return target_playlist_name
    return None


# Check if the target playlist exists in the schema
playlist_name_in_schema = find_playlist_in_schema(schema, target_playlist_name)
if playlist_name_in_schema:
    # Get the playlist from iTunes
    target_playlist = get_playlist(target_playlist_name)
    if target_playlist:
        # Add the song to the playlist
        add_song_to_playlist(song_path, target_playlist)
    else:
        print(f"Playlist '{target_playlist_name}' not found in iTunes.")
else:
    print(f"Playlist '{target_playlist_name}' not found in the schema.")
