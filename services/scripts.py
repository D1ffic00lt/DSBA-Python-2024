# Music recommendation application
from collections.abc import Callable
from typing import Generator
import pandas as pd
from collections import defaultdict
from .cfg import TableIndexes, MUSICALITY_ROWS_NORM, MUSICALITY_ROWS



class Song:
    def __init__(self, row: pd.Series) -> None:
        self.id = row.index
        self.track = row.Track
        self.album = row.Album
        self.artist = row.Artist

        self.musicality = row[MUSICALITY_ROWS_NORM].values

    def __repr__(self):
        return f"|{self.artist}: {self.track}|\n"

    def eff_distance(self, other: "Song") -> float:
        """Calculate the effective distance between two songs based on their musicality.

        This method computes the Euclidean distance between the musicality attributes of 
        the current song and another song. The distance is calculated as the square root 
        of the sum of the squared differences of their musicality values.

        Args:
            other: Another instance of the Song class to compare against.

        Returns:
            The effective distance as a float value.
        """

        return (
            sum(
                (
                    (other.musicality[i] - self.musicality[i]) ** 2
                    for i in range(len(self.musicality))
                )
            )
            ** 0.5
        )


class DataBase:
    def __init__(self, filename: str) -> None:
        self._storage = defaultdict(lambda: [])
        self._filepath: str = filename

        self.load()

    @property
    def songs(self) -> list[Song]:
        return sum(self._storage.values(), start=[])

    @staticmethod
    def _normalize_musicality_rows(df: pd.DataFrame) -> None:
        for row in MUSICALITY_ROWS:
            df.loc[:, f"{row}_norm"] = (df[row] - df[row].min()) / (
                df[row].max() - df[row].min()
            )

    def load(self) -> None:
        df = pd.read_csv(self._filepath, index_col=0)
        df.dropna(subset=MUSICALITY_ROWS, inplace=True)
        print(len(df.Album.unique()))
        self._normalize_musicality_rows(df)
        for _, row in df.iterrows():
            self.add_song(Song(row))

    def add_song(self, song: Song) -> None:
        self._storage[song.artist].append(song)

    def search(self, request: str) -> list[Song]:
        return [
            song
            for song in sum(self._storage.values(), start=[])
            if request in song.track
        ]

    def similar_songs(self, song: Song, count: int = 5) -> list[Song]:
        """Retrieve a list of songs that are similar to a given song.

        This method identifies and returns a specified number of songs that are most 
        similar to the provided song based on their effective distance in musicality. 
        The similarity is determined by sorting the songs according to their distance 
        from the given song and selecting the closest matches.

        Args:
            song: The Song instance to compare against.
            count: The maximum number of similar songs to return (default is 5).

        Returns:
            A list of Song instances that are similar to the provided song.
        """
        return [
            i[0]
            for i in list(
                sorted(
                    [
                        (_song, _song.eff_distance(song))
                        for _song in self.songs
                        if _song != song
                    ],
                    key = lambda x: x[1],
                )[:count]
            )
        ]
        
    def get_songs_by_artist(self, artist: str) -> list[Song]:
        return self._storage.get(artist, [])
    
    def filter(self, match_: list[Callable] | Callable, count: int = -1, mode: Callable = all) -> Generator[Song, None, None]:
        if isinstance(match_, Callable):
            match_ = [match_]
        return_counter = 0
        for song in self.songs:
            if return_counter == count:
                break
            match = [i(song) for i in match_]
            if mode(match):
                return_counter += 1
                yield song
            


def get_top_artists(data: list[list[str]], n: int) -> list[tuple[str, float]]:
    artists = {}
    likes = {}

    for row in data:
        artists[row[TableIndexes.ARTIST.value]] = (
            artists.get(row[TableIndexes.ARTIST.value], 0) + 1
        )
        likes[row[TableIndexes.ARTIST.value]] = (
            likes.get(row[TableIndexes.ARTIST.value], 0)
            + float(row[TableIndexes.LIKES.value])
            if row[TableIndexes.LIKES.value] != ""
            else 0
        )

    for artist in artists:
        artists[artist] = likes[artist] / artists[artist]

    return sorted(artists.items(), key=lambda x: x[1], reverse=True)[:n]


def get_minimum_and_maximum(data: list[list[str]], index: int) -> tuple[float, float]:
    if index < 0 or index >= len(data[0]):
        raise IndexError("Index out of range")

    if not data[0][index].replace(".", "", 1).isdigit():
        raise ValueError("Column must be a digit")

    column = [float(row[index]) for row in data if row[index]]
    return min(column), max(column)


def get_shape(data: list[list[str]]) -> tuple[int, int]:
    return len(data), len(data[0])

