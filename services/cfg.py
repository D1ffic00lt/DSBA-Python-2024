from enum import Enum
from typing import Final


class TableIndexes(Enum):
    ID = 0
    ARTIST = 1
    URL_SPOTIFY = 2
    TRACK = 3
    ALBUM = 4
    ALBUM_TYPE = 5
    URI = 6
    LIKES = 22

    # Danceability
    # Energy
    # Key
    # Loudness
    # Speechiness
    # Acousticness
    # Instrumentalness
    # Liveness
    # Valence
    # Tempo
    # Duration_ms
    # Url_youtube
    # Title
    # Channel
    # Views
    # Likes
    # Comments
    # Description
    # Licensed
    # official_video
    # Stream
    
MUSICALITY_ROWS: Final[list[str]] = [
    "Danceability",
    "Energy",
    "Key",
    "Loudness",
    "Speechiness",
    "Acousticness",
    "Instrumentalness",
    "Liveness",
    "Valence",
    "Tempo",
    "Duration_ms",
]

MUSICALITY_ROWS_norm: Final[list[str]] = [f"{row}_norm" for row in MUSICALITY_ROWS]
