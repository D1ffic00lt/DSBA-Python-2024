# Music recommendation application
import pandas as pd
from collections import defaultdict
from cfg import TableIndexes


class Song:
    def __init__(self, row: pd.Series) -> None:
        self.id = row.index
        self.track = row.Track
        self.album = row.Album
        self.artist = row.Artist
        
    def __repr__(self):
        return f'|{self.artist}: {self.track}|\n'


class DataBase:
    def __init__(self, filename: str) -> None:
        self._storage = defaultdict(lambda: [])
        df = pd.read_csv(filename, index_col=0)
        
        for _, row in df.iterrows():
            self.add_song(
                Song(row)       
            )
        

    def add_song(self, song: Song) -> None:
        self._storage[song.artist].append(song)

    def get_song(self, song_id: int) -> Song | None:
        return self._storage.get(song_id)

    def search(self, request: str) -> list[Song]:
        _result = []
        for song in sum(self._storage.values(), start=[]):
            if request in song.track:
                _result.append(song)
        return _result
    
        
            
            
            
            
        

def get_top_artists(data: list[list[str]], n: int) -> list[tuple[str, float]]:
    artists = {}
    likes = {}

    for row in data:
        artists[row[TableIndexes.ARTIST.value]] = artists.get(row[TableIndexes.ARTIST.value], 0) + 1
        likes[row[TableIndexes.ARTIST.value]] = (
            likes.get(row[TableIndexes.ARTIST.value], 0) + float(row[TableIndexes.LIKES.value])
            if row[TableIndexes.LIKES.value] != ""
            else 0
        )

    for artist in artists:
        artists[artist] = likes[artist] / artists[artist]

    return sorted(artists.items(), key=lambda x:x[1], reverse=True)[:n]


def get_minimum_and_maximum(data: list[list[str]], index: int) -> tuple[float, float]:
    if index < 0 or index >= len(data[0]):
        raise IndexError("Index out of range")

    if not data[0][index].replace(".", "", 1).isdigit():
        raise ValueError("Column must be a digit")

    column = [float(row[index]) for row in data if row[index]]
    return min(column), max(column)


def get_shape(data: list[list[str]]) -> tuple[int, int]:
    return len(data), len(data[0])

if __name__ == '__main__':
    db = DataBase('./data/Spotify_Youtube.csv')
    print(db.search('asFGAERT QWERT A DGADG Wr f'))
