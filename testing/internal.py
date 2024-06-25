import subprocess

def add_file_to_itunes_playlist(file_path, playlist_name):
    # Path to the VBScript file
    vbs_file_path = '../to-itunes.vbs'

    # Command to run the VBScript with arguments
    command = ['cscript', vbs_file_path, file_path, playlist_name]

    # Execute the VBScript
    result = subprocess.run(command, capture_output=True, text=True)

    # Print the output from the VBScript
    print(result.stdout)
    print(result.stderr)

# Example usage
file_path = r'C:\Users\danie\Music\Hello.mp3'
playlist_name = 'House-'
add_file_to_itunes_playlist(file_path, playlist_name)
