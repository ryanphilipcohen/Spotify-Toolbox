from fastapi import APIRouter, HTTPException, Request, Header, Depends

from backend.app.models.web.user import SpotifyLogin
from backend.database import get_connection
from backend.auth import create_access_token
from backend.auth import get_current_user

router = APIRouter()


@router.get("/users")
def get_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, spotify_id, date_created FROM user")
    users = cursor.fetchall()

    conn.close()

    return [
        {"id": user[0], "spotify_id": user[1], "date_created": user[2]}
        for user in users
    ]


@router.get("/current")
def get_current_user(user_id: str = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, spotify_id, date_created FROM user WHERE id = ?",
        (user_id,),
    )
    user = cursor.fetchone()
    conn.close()
    if user:
        return {
            "user": {
                "id": user[0],
                "spotify_id": user[1],
                "date_created": user[2],
            }
        }
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/spotify-login")
def spotify_login(data: dict):
    spotify_id = data.get("spotify_id")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM user WHERE spotify_id = ?", (spotify_id,))
    result = cursor.fetchone()

    if result:
        user_id = result[0]
    else:
        cursor.execute("INSERT INTO user (spotify_id) VALUES (?)", (spotify_id,))
        conn.commit()
        user_id = cursor.lastrowid

    conn.close()
    # Return JWT for your app
    token = create_access_token({"user_id": user_id})
    return {"app_access_token": token, "user_id": user_id}
