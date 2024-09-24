# Music recommendation application
import csv

from cfg import TableIndexes


class Song:
    def __init__(self, row: list[str]) -> None:
        self.id = row[TableIndexes.ID.value]
        self.name = row[TableIndexes.TRACK.value]
        self.album = row[TableIndexes.ALBUM.value]
        self.artist = row[TableIndexes.ARTIST.value]


class DataBase:
    def __init__(self, filename: str) -> None:
        self.db = {}

        with open(filename, encoding='utf-8-sig') as file:
            _ = file.readline()
            reader = csv.reader(file)

            for row in reader:
                self.add_song(self.__parse_row(row))

    @staticmethod
    def __parse_row(row: list[str]) -> Song:
        row[TableIndexes.ID.value] = int(row[TableIndexes.ID.value])

        return Song(row)

    def add_song(self, song: Song) -> None:
        if song.id in self.db:
            raise 'A song with this id already exists!'

        self.db[song.id] = song

    def get_song(self, song_id: int) -> Song | None:
        return self.db.get(song_id)


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
    db = DataBase(filename='../data/Spotify_Youtube.csv')

    print(db.get_song(1).name)
