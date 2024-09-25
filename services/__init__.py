from .scripts import get_shape, get_minimum_and_maximum, get_top_artists, DataBase, Song

if __name__ == '__main__':
    db = DataBase(filename='../data/Spotify_Youtube.csv')

    song = db.get_song(1)

    print(song.name if song else 'Song does not exist')

