from pydantic import BaseModel


class SpotifyLogin(BaseModel):
    spotify_id: str
