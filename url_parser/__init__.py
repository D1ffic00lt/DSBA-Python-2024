import datetime
import json
from urllib import response
import requests
import threading
from bs4 import BeautifulSoup as BS
from datetime import datetime
# from .cfg import LAST_FM_URL

LAST_FM_URL = "https://www.last.fm/music/"


class AuthorMetadataParser(object):

    def __init__(self, author: str, db) -> None:
        self.author = author
        self.db = db

        self._metadata = {}
        self._responses = {}

        for song in db.get_songs_by_artist(author):
            # song_url = f"{LAST_FM_URL}{author}/_/{song.title}"
            album_url = f"{LAST_FM_URL}{author}/{song.album}"
            self._parse_metadata(self.make_request(album_url))

            # self._responses[song] = BS(album_response.text, "html.parser")

    @staticmethod
    def make_request(url: str) -> str:
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(
                f"Failed to retrieve metadata from {url}: {response.status_code}"
            )

        return response.text

    def _parse_metadata(self, album_response: str):
        bs = BS(album_response, "html.parser")
        div_metadata = bs.find("div", {"class": "metadata-column hidden-xs"})
        if not div_metadata:
            return

        div_metadata = div_metadata.find("dl", {"class": "catalogue-metadata"})
        date = div_metadata.find_all("dd", {"class": "catalogue-metadata-description"})[
            -1
        ].text.strip()
        return datetime.strptime(date, "%d %B %Y").date().strftime("%d/%m/%Y")


