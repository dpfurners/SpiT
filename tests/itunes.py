import json
import unittest
import xml.etree.ElementTree as ET


class TestiTunesPlaylists(unittest.TestCase):
    def setUp(self):
        # Load the JSON scheme
        with open('scheme.json', 'r') as f:
            self.scheme = json.load(f)

        # Parse the iTunes XML file
        self.itunes_playlists = self.parse_itunes_xml(r'C:\Users\danie\Music\iTunes\iTunes Music Library.xml')

    def parse_itunes_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        playlists = []
        for dict_elem in root.findall(".//dict"):
            keys = list(dict_elem)
            for i, key_elem in enumerate(keys):
                if key_elem.tag == "key" and key_elem.text == "Name":
                    if i + 1 < len(keys):
                        name_elem = keys[i + 1]
                        if name_elem.tag == "string":
                            playlists.append(name_elem.text)
        return playlists

    def get_itunes_playlists_from_scheme(self, scheme):
        playlists = []
        for key, value in scheme.items():
            if isinstance(value, dict):
                playlists.extend(self.get_itunes_playlists_from_scheme(value))
            elif key == "itunes":
                playlists.append(value)
        return playlists

    def test_all_playlists_in_itunes(self):
        scheme_playlists = self.get_itunes_playlists_from_scheme(self.scheme)
        for playlist in scheme_playlists:
            with self.subTest(playlist=playlist):
                self.assertIn(playlist, self.itunes_playlists, f"Playlist {playlist} is not in iTunes library")


if __name__ == '__main__':
    unittest.main()
