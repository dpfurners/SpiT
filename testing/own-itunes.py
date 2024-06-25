import xml.etree.ElementTree as ET
from xml.dom import minidom


# Function to prettify the XML
def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


# Create the root element
root = ET.Element("plist", version="1.0")
dict_elem = ET.SubElement(root, "dict")

# Add standard iTunes library keys
ET.SubElement(dict_elem, "key").text = "Major Version"
ET.SubElement(dict_elem, "integer").text = "1"

ET.SubElement(dict_elem, "key").text = "Minor Version"
ET.SubElement(dict_elem, "integer").text = "1"

ET.SubElement(dict_elem, "key").text = "Date"
ET.SubElement(dict_elem, "date").text = "2023-06-18T12:00:00Z"

ET.SubElement(dict_elem, "key").text = "Application Version"
ET.SubElement(dict_elem, "string").text = "12.9.5.5"

ET.SubElement(dict_elem, "key").text = "Features"
ET.SubElement(dict_elem, "integer").text = "5"

ET.SubElement(dict_elem, "key").text = "Show Content Ratings"
ET.SubElement(dict_elem, "true")

ET.SubElement(dict_elem, "key").text = "Music Folder"
ET.SubElement(dict_elem, "string").text = "file://localhost/C:/Users/danie/Music/iTunes/iTunes%20Media/"

# Add Tracks dictionary
ET.SubElement(dict_elem, "key").text = "Tracks"
tracks_dict = ET.SubElement(dict_elem, "dict")


# Function to add a track
def add_track(track_id, track_info):
    track_key = ET.SubElement(tracks_dict, "key")
    track_key.text = str(track_id)
    track_dict = ET.SubElement(tracks_dict, "dict")

    for key, value in track_info.items():
        key_elem = ET.SubElement(track_dict, "key")
        key_elem.text = key
        if isinstance(value, bool):
            value_elem = ET.SubElement(track_dict, "true" if value else "false")
        elif isinstance(value, int):
            value_elem = ET.SubElement(track_dict, "integer")
            value_elem.text = str(value)
        elif isinstance(value, str):
            value_elem = ET.SubElement(track_dict, "string")
            value_elem.text = value
        elif isinstance(value, float):
            value_elem = ET.SubElement(track_dict, "real")
            value_elem.text = str(value)


# Example track info
track_info_example = {
    "Track ID": 4444,
    "Name": "Example Song",
    "Artist": "Example Artist",
    "Album": "Example Album",
    "Genre": "Example Genre",
    "Kind": "MPEG audio file",
    "Size": 12345678,
    "Total Time": 300000,
    "Track Number": 1,
    "Year": 2023,
    "Date Added": "2023-06-18T12:00:00Z",
    "Bit Rate": 256,
    "Sample Rate": 44100,
    "Play Count": 1,
    "Play Date": 3600000000,
    "Play Date UTC": "2023-06-18T12:00:00Z",
    "Skip Count": 0,
    "Skip Date": "2023-06-18T12:00:00Z",
    "Release Date": "2023-06-18T12:00:00Z",
    "Compilation": False
}

# Add example track to library
add_track(1234, track_info_example)

# Save the new XML to a file
with open("my_iTunes_Library.xml", "w", encoding="utf-8") as f:
    f.write(prettify(root))

print("New iTunes Library created successfully.")
