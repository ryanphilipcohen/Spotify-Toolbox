from pydantic import BaseModel


class TrackIn(BaseModel):
    user_id: int | None = None
    track_index: int
    name: str
    image: str
    spotify_id: str


class TrackOut(TrackIn):
    pass
