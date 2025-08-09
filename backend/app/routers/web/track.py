from fastapi import APIRouter, Header, Body, HTTPException, Query
from backend.app.models.web.track import TrackIn, TrackOut
from backend.database import get_connection
from typing import Optional

router = APIRouter()


@router.post("/")
def create_track(track: TrackIn):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO track (user_id, added_at, name, image, spotify_id) VALUES (?, ?)",
        (track.user_id, track.added_at, track.name, track.image, track.spotify_id),
    )

    conn.commit()
    conn.close()

    return TrackOut(
        user_id=track.user_id,
        added_at=track.added_at,
        name=track.name,
        image=track.image,
        spotify_id=track.spotify_id,
    )


@router.get("/")
def get_track(track: TrackIn):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name FROM track WHERE user_id = ? AND added_at = ?",
        (track.user_id, track.added_at),
    )
    track_data = cursor.fetchone()

    conn.commit()
    conn.close()

    return (
        TrackOut(
            user_id=track.user_id,
            added_at=track.added_at,
            name=track_data[1],
            image=track.image,
            spotify_id=track.spotify_id,
        )
        if track_data
        else None
    )


@router.get("/tracks")
def get_tracks(
    start: Optional[int] = Query(None, ge=0),
    end: Optional[int] = Query(None, ge=0),
    sort_by: Optional[str] = Query(None, regex="^(added_at|name)$"),
    order: Optional[str] = Query("desc", regex="^(asc|desc)$"),
    user_id: int = Header(...),
):
    conn = get_connection()
    cursor = conn.cursor()

    # Base query
    query = """
        SELECT id, user_id, added_at, name, image, spotify_id"""
    query += " FROM track WHERE user_id = ?"
    params = [user_id]

    # Add sorting
    if sort_by:
        query += f" ORDER BY {sort_by} {order.upper()}"  # type: ignore

    cursor.execute(query, params)
    all_data = cursor.fetchall()

    # Bounds checking
    total_len = len(all_data)
    if start is None:
        start = 0
    if end is None or end > total_len:
        end = total_len

    sliced_data = all_data[start:end]

    conn.close()

    return [
        TrackOut(
            user_id=row[1],
            added_at=row[2],
            name=row[3],
            image=row[4],
            spotify_id=row[5],
        )
        for row in sliced_data
    ]


@router.post("/sync-tracks")
def sync_tracks(user_id: int = Header(...), tracks: list[TrackIn] = Body(...)):
    conn = get_connection()
    cursor = conn.cursor()

    for track in tracks:
        cursor.execute(
            """
                INSERT INTO track (user_id, added_at, name, image, spotify_id)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id, added_at) DO UPDATE SET
                    name = excluded.name,
                    image = excluded.image,
                    spotify_id = excluded.spotify_id
                """,
            (
                track.user_id,
                track.added_at,
                track.name,
                track.image,
                track.spotify_id,
            ),
        )

    cursor.execute(
        "SELECT id, user_id, added_at, name, image, spotify_id FROM track WHERE user_id = ?",
        (user_id,),
    )
    track_data = cursor.fetchall()

    conn.commit()
    conn.close()

    return [
        TrackOut(
            user_id=row[1],
            added_at=row[2],
            name=row[3],
            image=row[4],
            spotify_id=row[5],
        )
        for row in track_data
        if row is not None
    ]
