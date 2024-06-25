' AddFileToPlaylist.vbs
Dim iTunesApp, playlist, newTracks
Set iTunesApp = CreateObject("iTunes.Application")

' Get command line arguments
Set objArgs = WScript.Arguments
filePath = objArgs(0)
playlistName = objArgs(1)

' Find the playlist by name
Set playlist = Nothing
For Each pl In iTunesApp.LibrarySource.Playlists
    If pl.Name = playlistName Then
        Set playlist = pl
        Exit For
    End If
Next

' Add the file to the playlist
If Not playlist Is Nothing Then
    Set newTracks = playlist.AddFile(filePath)
    ' Check if the file was added successfully
    If newTracks Is Nothing Then
        WScript.Echo "Failed to add the file to the playlist."
    Else
        WScript.Echo "File added successfully to the playlist '" & playlistName & "'."
    End If
Else
    WScript.Echo "Playlist '" & playlistName & "' not found."
End If

' Clean up
Set newTracks = Nothing
Set playlist = Nothing
Set iTunesApp = Nothing
