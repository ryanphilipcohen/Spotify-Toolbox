from fastapi import APIRouter, Header, Body, HTTPException, Query, Depends
from backend.app.models.web.track import TrackIn, TrackOut
from backend.database import get_connection
from typing import Optional
from backend.auth import get_current_user

router = APIRouter()


@router.post("/")
def create_track(track: TrackIn, user_id: str = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO track (
            user_id, added_at, name, artists, album, album_id,
            duration_ms, explicit, popularity, track_number,
            release_date, image, spotify_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            track.user_id,
            track.added_at,
            track.name,
            track.artists,
            track.album,
            track.album_id,
            track.duration_ms,
            track.explicit,
            track.popularity,
            track.track_number,
            track.release_date,
            track.image,
            track.spotify_id,
        ),
    )

    conn.commit()
    conn.close()

    return TrackOut(
        user_id=track.user_id,
        added_at=track.added_at,
        name=track.name,
        artists=track.artists,
        album=track.album,
        album_id=track.album_id,
        duration_ms=track.duration_ms,
        explicit=track.explicit,
        popularity=track.popularity,
        track_number=track.track_number,
        release_date=track.release_date,
        image=track.image,
        spotify_id=track.spotify_id,
    )


@router.get("/")
def get_track(track: TrackIn, user_id: str = Depends(get_current_user)):
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
            name=track.name,
            artists=track.artists,
            album=track.album,
            album_id=track.album_id,
            duration_ms=track.duration_ms,
            explicit=track.explicit,
            popularity=track.popularity,
            track_number=track.track_number,
            release_date=track.release_date,
            image=track.image,
            spotify_id=track.spotify_id,
        )
        if track_data
        else None
    )


"""
This function has a couple of parameters to function as a pagination and sorting mechanism.
sort_by and order use regex to limit the options available to the user.
Query and Optional are used to make the parameters optional, giving a default or specific options.
"""


@router.get("/tracks")
def get_tracks(
    start: Optional[int] = Query(None, ge=0),
    end: Optional[int] = Query(None, ge=0),
    sort_by: Optional[str] = Query(None, regex="^(added_at|name)$"),
    order: Optional[str] = Query("desc", regex="^(asc|desc)$"),
    user_id: str = Depends(get_current_user),
):
    conn = get_connection()
    cursor = conn.cursor()

    # Base query
    query = """
        SELECT id, user_id, name, artists, album, album_id, duration_ms,
               explicit, popularity, track_number, release_date, added_at,
                image, spotify_id  FROM track WHERE user_id = ?
    """
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
            name=row[2],
            artists=row[3],
            album=row[4],
            album_id=row[5],
            duration_ms=row[6],
            explicit=row[7],
            popularity=row[8],
            track_number=row[9],
            release_date=row[10],
            added_at=row[11],
            image=row[12],
            spotify_id=row[13],
        )
        for row in sliced_data
    ]


"""
Body is a list of TrackIn objects, and it's passed in the request body.
You use body when you want to send more complex data structures in the request.
"""


@router.post("/sync-tracks")
async def sync_tracks(
    tracks: list[TrackIn] = Body(...), user_id: str = Depends(get_current_user)
):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # first, remove all current tracks for the user
        # tracks that will have been deleted from the user's library must be removed here
        cursor.execute("DELETE FROM track WHERE user_id = ?", (user_id,))
        for track in tracks:
            cursor.execute(
                """
                INSERT INTO track (
                    user_id, added_at, name, artists, album, album_id,
                    duration_ms, explicit, popularity, track_number,
                    release_date, image, spotify_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id, added_at) DO UPDATE SET
                    name = excluded.name,
                    artists = excluded.artists,
                    album = excluded.album,
                    album_id = excluded.album_id,
                    duration_ms = excluded.duration_ms,
                    explicit = excluded.explicit,
                    popularity = excluded.popularity,
                    track_number = excluded.track_number,
                    release_date = excluded.release_date,
                    image = excluded.image,
                    spotify_id = excluded.spotify_id
                """,
                (
                    track.user_id,
                    track.added_at,
                    track.name,
                    track.artists,
                    track.album,
                    track.album_id,
                    track.duration_ms,
                    track.explicit,
                    track.popularity,
                    track.track_number,
                    track.release_date,
                    track.image,
                    track.spotify_id,
                ),
            )

        cursor.execute(
            """
            SELECT id, user_id, name, artists, album, album_id, duration_ms,
                explicit, popularity, track_number, release_date, added_at,
                image, spotify_id  FROM track WHERE user_id = ?
        """,
            (user_id,),
        )
        track_data = cursor.fetchall()
    except Exception as e:
        conn.rollback()  # this will undo any changes made to the database
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))

    conn.commit()
    conn.close()

    return [
        TrackOut(
            user_id=row[1],
            name=row[2],
            artists=row[3],
            album=row[4],
            album_id=row[5],
            duration_ms=row[6],
            explicit=row[7],
            popularity=row[8],
            track_number=row[9],
            release_date=row[10],
            added_at=row[11],
            image=row[12],
            spotify_id=row[13],
        )
        for row in track_data
        if row is not None
    ]
