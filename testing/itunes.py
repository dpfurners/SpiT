import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib
import numpy as np
from xml.etree import ElementTree as ET
from collections import defaultdict


tree = ET.parse(r"C:\Users\danie\Music\iTunes\iTunes Music Library.xml")
root = tree.getroot()

# Exploring contents of root
root_lst = []
for i, x in enumerate(root[0]):
    root_lst.append([x.text, x.tag])

root_frame = pd.DataFrame(root_lst, columns=['text', 'tag'])
print(root_frame)


# Exploring "Tracks" node
track_lst = []
for x in root[0][15]:
    track_lst.append([x.text, x.tag])

track_frame = pd.DataFrame(track_lst, columns = ['text', 'tag'])
print(track_frame)

# Exploring contents of the first track dict
song_lst = []
for x in root[0][15][1]:
    song_lst.append([x.text, x.tag])

track_frame = pd.DataFrame(song_lst, columns=['text', 'tag'])
print(track_frame)

columns = sorted(list(set([root[0][15][i][j].text for i, _ in enumerate(root[0][15]) for j, _ in enumerate(root[0][15][i]) if root[0][15][i][j].tag == 'key'])))
print(columns)

data = defaultdict(list)
bool_columns = ['Album Loved', 'Apple Music', 'Clean', 'Compilation', 'Explicit', 'HD', 'Has Video', 'Loved', 'Matched', 'Music Video', 'Part Of Gapless Album', 'Playlist Only']

for i, _ in enumerate(root[0][15]):
    temp_columns = list.copy(columns)
    if i % 2 == 1:
        for j, _ in enumerate(root[0][15][i]):
             if root[0][15][i][j].tag == 'key':
                if root[0][15][i][j].text in bool_columns:
                    data[root[0][15][i][j].text].append(root[0][15][i][j+1].tag)
                    temp_columns.remove(root[0][15][i][j].text)
                else:
                    data[root[0][15][i][j].text].append(root[0][15][i][j+1].text)
                    temp_columns.remove(root[0][15][i][j].text)
        for column in temp_columns:
            data[column].append(np.nan)

df = pd.DataFrame(data)
df.head()

numeric_columns = ['Artwork Count', 'Bit Rate', 'Disc Count', 'Disc Number', 'Play Count', 'Play Date', 'Sample Rate', 'Size', 'Skip Count', 'Track Count', 'Track ID', 'Track Number', 'Year']
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)

date_columns = ['Date Added', 'Date Modified', 'Play Date UTC', 'Release Date', 'Skip Date']
df[date_columns] = df[date_columns].apply(pd.to_datetime)

print(df)
