from __future__ import annotations

import os
import typing
from dataclasses import dataclass, field
from typing import List, Optional, Union
from lxml import etree as ET

if typing.TYPE_CHECKING:
    from spotify import SPlaylist

TRACK_REQUESTED_KEYS = ("Name", "Artist", "Album")
LIBRARY_EXCLUDED = ("Downloaded", "Music", "Podcasts", "Movies", "TV Shows", "Audiobooks", "Genius", "Library")
ROOT_FOLDERS = ("Auflegen", "Private", "Tanzen")


@dataclass
class ItunesObject:
    iid: int
    name: str


@dataclass
class ITrack(ItunesObject):
    artist: str = None
    album: str = None

    def __eq__(self, other):
        if isinstance(other, ITrack):
            if other.iid == self.iid:
                return True
        if isinstance(other, int):
            if other == self.iid:
                return True
        return False


@dataclass
class IPlaylist(ItunesObject):
    liid: str
    parent: Optional[IFolder, ILibrary]
    tracks: List[ITrack]
    spotify: bool = False
    reference: "SPlaylist" = None

    def __eq__(self, other):
        if isinstance(other, IFolder):
            if other.iid == self.iid:
                return True
        if len(other) == 16:
            if other == self.liid:
                return True
        if isinstance(other, int):
            if other == self.iid:
                return True
        return False


@dataclass
class IFolder(ItunesObject):
    liid: str
    parent: Optional[IFolder, ILibrary]
    children: List[Union["IFolder", IPlaylist]] = field(default_factory=list)

    def __eq__(self, other):
        if isinstance(other, IFolder):
            if other.iid == self.iid:
                return True
        if len(other) == 16:
            if other == self.liid:
                return True

        if isinstance(other, int):
            if other == self.iid:
                return True
        return False


class ILibrary:
    def __init__(self, name: str, playlists: list[IPlaylist] = None):
        if playlists is None:
            playlists = []
        self.name = name
        self.playlists = playlists
        self.folders = []

    @classmethod
    def parse_library(cls, library_file: str = r"C:\Users\danie\Music\iTunes\iTunes Music Library.xml",
                      reference_file: str = None) -> "ILibrary":
        if library_file is None:
            library_file = os.getenv("ITUNES_LIBRARY")

        tree = ET.parse(library_file)
        root = tree.getroot()

        library = cls(library_file.split("\\")[0].rstrip(".xml"))

        tracks = []

        # Extract tracks
        for dict_entry in root.findall("./dict/dict/dict"):
            track_id = None
            track_info = {}
            keys = {}

            for i in range(0, len(dict_entry), 2):
                key = dict_entry[i].text
                value = dict_entry[i + 1].text
                keys[key] = ""
                if key == "Track ID":
                    track_id = int(value)
                else:
                    track_info[key] = value

            if track_id:
                requested = {x.lower(): track_info[x] for x in TRACK_REQUESTED_KEYS if x in track_info.keys()}
                tracks.append(ITrack(track_id, **requested))

        missing_parents = {}

        # Extract playlists and their tracks
        for playlist in root.xpath("//dict[key='Playlist ID']"):
            playlist_id = playlist.xpath("string(key[.='Playlist ID']/following-sibling::*[1])")
            if playlist_id:
                playlist_id = int(playlist_id)
            playlist_name = playlist.xpath("string(key[.='Name']/following-sibling::*[1])")
            folder = bool(playlist.xpath("key[.='Folder']/following-sibling::*[1]"))
            parent_persistent_id = playlist.xpath("string(key[.='Parent Persistent ID']/following-sibling::*[1])")
            playlist_persistent_id = playlist.xpath("string(key[.='Playlist Persistent ID']/following-sibling::*[1])")

            if playlist_name in LIBRARY_EXCLUDED:
                continue

            playlist_items = playlist.xpath("key[.='Playlist Items']/following-sibling::array[1]")

            if folder:
                new_folder = IFolder(
                    iid=playlist_id,
                    name=playlist_name,
                    liid=playlist_persistent_id,
                    parent=None,
                    children=[]
                )
                if parent_persistent_id:
                    parent_folder = library.find_item(parent_persistent_id)
                    if parent_folder:
                        parent_folder.children.append(new_folder)
                        new_folder.parent = parent_folder
                    else:
                        if new_folder.name in ROOT_FOLDERS:
                            library.folders.append(new_folder)
                        else:
                            if parent_persistent_id in missing_parents.keys():
                                missing_parents[parent_persistent_id].append(new_folder)
                            else:
                                missing_parents[parent_persistent_id] = [new_folder]
                else:
                    if new_folder.name in ROOT_FOLDERS:
                        library.folders.append(new_folder)

                if playlist_persistent_id in missing_parents:
                    children = missing_parents.pop(playlist_persistent_id)
                    new_folder.children.extend(children)
            else:
                playlist_tracks = []
                if playlist_items:
                    for item in playlist_items[0].xpath("dict"):
                        track_id = int(item.xpath("string(key[.='Track ID']/following-sibling::*[1])"))
                        track = next((track for track in tracks if track == track_id), None)
                        if track:
                            playlist_tracks.append(track)
                new_playlist = IPlaylist(
                    iid=playlist_id,
                    name=playlist_name,
                    liid=playlist_persistent_id,
                    parent=None,
                    tracks=playlist_tracks
                )
                if parent_persistent_id:
                    parent_folder = library.find_item(parent_persistent_id)
                    if parent_folder:
                        parent_folder.children.append(new_playlist)
                        new_playlist.parent = parent_folder
                    else:
                        if parent_persistent_id in missing_parents.keys():
                            missing_parents[parent_persistent_id].append(new_playlist)
                        else:
                            missing_parents[parent_persistent_id] = [new_playlist]
        return library

    def find_item(self, criteria: str) -> Optional[IFolder]:
        for folder in self.folders:
            if isinstance(criteria, int):
                if folder.iid == criteria:
                    return folder
            elif isinstance(criteria, str):
                if folder.liid == criteria:
                    return folder
            found = self._find_folder_recursively(folder, criteria)
            if found:
                return found
        return None

    def _find_folder_recursively(self, parent_folder: IFolder, criteria: str) -> Optional[IFolder, IPlaylist]:
        for child in parent_folder.children:
            if isinstance(child, IFolder):
                if isinstance(criteria, int):
                    if child.iid == criteria:
                        return child
                elif isinstance(criteria, str):
                    if child.liid == criteria:
                        return child
                found = self._find_folder_recursively(child, criteria)
                if found:
                    return found
            elif isinstance(child, IPlaylist):
                if isinstance(criteria, int):
                    if child.iid == criteria:
                        return child
                elif isinstance(criteria, str):
                    if child.liid == criteria:
                        return child
        return None


if __name__ == '__main__':
    library = ILibrary.parse_library()
