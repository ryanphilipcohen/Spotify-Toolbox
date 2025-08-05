from pydantic import BaseModel


class TrackIn(BaseModel):
    user_id: int | None = None
    added_at: str
    name: str
    image: str
    spotify_id: str


class TrackOut(TrackIn):
    pass
