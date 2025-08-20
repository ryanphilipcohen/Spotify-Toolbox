from pydantic import BaseModel


class TrackIn(BaseModel):
    user_id: int
    name: str
    artists: str
    album: str
    album_id: str
    duration_ms: int
    explicit: bool
    popularity: int
    track_number: int
    release_date: str
    added_at: str
    image: str | None = None
    spotify_id: str


class TrackOut(TrackIn):
    pass
