# Music recommendation application
import csv

from cfg import TableEnum


class Song:
    def __init__(self, row: list[str]) -> None:
        self.id = int(row[TableEnum.ID.value])
        self.name = row[TableEnum.Track.value]
        self.album = row[TableEnum.Album.value]
        self.artist = row[TableEnum.Artist.value]


class DataBase:
    def __init__(self, filename):
        self.db = {}

        with open(filename, encoding='utf-8-sig') as file:
            _ = file.readline()
            reader = csv.reader(file)

            for row in reader:
                self.add_song(Song(row))

    def add_song(self, song: Song) -> None:
        self.db[song.id] = song

    def get_song(self, song_id: int) -> Song:
        return self.db.get(song_id)


if __name__ == '__main__':
    db = DataBase(filename='../data/Spotify_Youtube.csv')

    print(db.get_song(1).name)


def get_top_artists(data: list[list[str]], n: int) -> list[tuple[str, float]]:
    artists = {}
    likes = {}
    for row in data:
        artists[row[TableEnum.Artist.value]] = artists.get(row[TableEnum.Artist.value], 0) + 1
        likes[row[TableEnum.Artist.value]] = (
            likes.get(row[TableEnum.Artist.value], 0) + float(row[TableEnum.Likes.value])
            if row[TableEnum.Likes.value] != ""
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
