from fastapi import APIRouter, Depends, Request, HTTPException
import requests

from backend.auth import get_current_user

router = APIRouter()


# this is just a fake function to show how authentication will work
@router.post("/spotify/sync-tracks")
def sync_tracks(request: Request, user_id: str = Depends(get_current_user)):

    spotify_token = request.headers.get("Spotify-Token")
    if not spotify_token:
        raise HTTPException(status_code=400, detail="Missing Spotify token")

    headers = {"Authorization": f"Bearer {spotify_token}"}

    # Fetch all tracks from spotify
    # send to a track backend endpoint to add to the database
    # make sure that the track endpoint is checking per user and if the track doesn't exist already.

    # ...

    return
