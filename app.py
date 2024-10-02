

if __name__ == "__main__":
    from services import DataBase
    from url_parser import AuthorMetadataParser
    db = DataBase("./data/Spotify_Youtube.csv")
    author = "Muse"
    print(list(db.filter([lambda x: x.artist == author, lambda x: "hole" in x.track.lower()], mode=all)))