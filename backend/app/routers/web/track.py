from fastapi import APIRouter
from backend.app.models.web.track import TrackIn, TrackOut
from backend.database import get_connection

router = APIRouter()


@router.post("/")
def create_track(track: TrackIn):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO track (user_id, track_index, name, image, spotify_id) VALUES (?, ?)",
        (track.user_id, track.track_index, track.name, track.image, track.spotify_id),
    )

    conn.commit()
    conn.close()

    return TrackOut(
        user_id=track.user_id,
        track_index=track.track_index,
        name=track.name,
        image=track.image,
        spotify_id=track.spotify_id,
    )


@router.get("/")
def get_track(track: TrackIn):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name FROM track WHERE user_id = ? AND track_index = ?",
        (track.user_id, track.track_index),
    )
    track_data = cursor.fetchone()

    conn.commit()
    conn.close()

    return (
        TrackOut(
            user_id=track.user_id,
            track_index=track.track_index,
            name=track_data[1],
            image=track.image,
            spotify_id=track.spotify_id,
        )
        if track_data
        else None
    )


@router.get("/tracks")
def get_tracks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, user_id, track_index, name, image, spotify_id FROM track"
    )
    track_data = cursor.fetchone()

    conn.commit()
    conn.close()

    return (
        [
            TrackOut(
                user_id=row[1],
                track_index=row[2],
                name=row[3],
                image=row[4],
                spotify_id=row[5],
            )
            for row in track_data
            if row is not None
        ]
        if track_data
        else []
    )
