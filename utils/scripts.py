# Music recommendation application
import csv

ARTIST_INDEX = 1
LIKES_INDEX = 22

def get_top_artists(data: list[list[str]], n: int) -> list[tuple[str, float]]:
    artists = dict()
    likes = dict()
    for row in data:
        artists[row[ARTIST_INDEX]] = artists.get(row[ARTIST_INDEX], 0) + 1
        likes[row[ARTIST_INDEX]] = (
            likes.get(row[ARTIST_INDEX], 0) + float(row[LIKES_INDEX])
            if row[LIKES_INDEX] != ""
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

def read_from_file(filename: str = "./data/Spotify_Youtube.csv"):
    with open(filename) as file:
        header = file.readline()
        reader = csv.reader(file)
        data = [row for row in reader]
    return header, data
