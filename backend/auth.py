from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"  # Hardcoded temporarily
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# This will read headers sent by the client that include the app token
security = HTTPBearer()

"""
Creates a JWT, or JavaScript Web Token, for the user to authenticate future requests.
This is a token just like the one spotify generates for you, but is for the app to
allow messages to the backend.

In user.py, the user_id is passed into this function to be encoded into the token.
Encoding is done with an algorithm and a secret key, as well as the expiration time.
"""


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


"""
The header of a request contains the token, extracted by HTTPBearer.
The token is decoded with the same key and algorithm.
If the token is valid, the user_id is returned.
"""


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
